"""Small LangGraph workflow for transaction inspection."""

from collections.abc import Callable, Iterable
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from banking_ai.models import AgentState, BankingTransaction, InspectionResult
from banking_ai.ollama_client import OllamaClient
from banking_ai.rules import inspect_transaction_rules

StreamWriter = Callable[[str], None]


class GraphState(TypedDict, total=False):
    transaction: BankingTransaction
    findings: list
    suspicious: bool
    ai_explanation: str
    final_result: InspectionResult | None


def build_explanation_prompt(state: AgentState) -> str:
    transaction = state.transaction
    finding_lines = (
        "\n".join(f"- {finding.rule_id}: {finding.reason}" for finding in state.findings)
        or "- no deterministic rule was triggered"
    )
    status = "SUSPICIOUS" if state.suspicious else "NORMAL"
    rule_instruction = (
        "The rule findings listed above were triggered. Do not say that no rule was triggered."
        if state.findings
        else "No deterministic rule was triggered."
    )

    return f"""You are explaining a local learning example, not making a real banking decision.

Transaction:
- id: {transaction.transaction_id}
- account: {transaction.account_id}
- amount: {transaction.amount} {transaction.currency}
- merchant: {transaction.merchant}
- country: {transaction.country}
- type: {transaction.transaction_type}
- timestamp: {transaction.timestamp.isoformat()}

Deterministic rule status: {status}
Rule findings:
{finding_lines}
Rule instruction: {rule_instruction}

Write a short plain-language inspection. Include:
1. whether this looks normal or suspicious
2. why
3. which fields mattered
4. which rule was triggered, if any
5. what a human reviewer should check
"""


def load_transaction_node(state: GraphState) -> GraphState:
    transaction = state["transaction"]
    return AgentState(transaction=transaction).model_dump()


def apply_rules_node(state: GraphState) -> GraphState:
    agent_state = AgentState.model_validate(state)
    findings = inspect_transaction_rules(agent_state.transaction)
    agent_state.findings = findings
    agent_state.suspicious = bool(findings)
    return agent_state.model_dump()


def finalize_result_node(state: GraphState) -> GraphState:
    agent_state = AgentState.model_validate(state)
    status = "SUSPICIOUS" if agent_state.suspicious else "NORMAL"
    reviewer_check = (
        "Review the triggered rule fields and compare the transaction with normal customer behavior."
        if agent_state.suspicious
        else "No deterministic rule was triggered; spot-check normal account context if needed."
    )
    agent_state.final_result = InspectionResult(
        transaction_id=agent_state.transaction.transaction_id,
        status=status,
        findings=agent_state.findings,
        ai_explanation=agent_state.ai_explanation,
        reviewer_check=reviewer_check,
    )
    return agent_state.model_dump()


def make_generate_ai_explanation_node(
    ollama_client: OllamaClient,
    stream_writer: StreamWriter | None = None,
) -> Callable[[GraphState], GraphState]:
    def generate_ai_explanation_node(state: GraphState) -> GraphState:
        agent_state = AgentState.model_validate(state)
        prompt = build_explanation_prompt(agent_state)
        chunks: list[str] = []

        for chunk in ollama_client.stream_generate(prompt):
            chunks.append(chunk)
            if stream_writer:
                stream_writer(chunk)

        agent_state.ai_explanation = "".join(chunks).strip()
        return agent_state.model_dump()

    return generate_ai_explanation_node


def build_inspection_graph(
    ollama_client: OllamaClient,
    stream_writer: StreamWriter | None = None,
) -> Any:
    graph = StateGraph(GraphState)
    graph.add_node("load_transaction", load_transaction_node)
    graph.add_node("apply_rules", apply_rules_node)
    graph.add_node(
        "generate_ai_explanation",
        make_generate_ai_explanation_node(ollama_client, stream_writer),
    )
    graph.add_node("finalize_result", finalize_result_node)

    graph.set_entry_point("load_transaction")
    graph.add_edge("load_transaction", "apply_rules")
    graph.add_edge("apply_rules", "generate_ai_explanation")
    graph.add_edge("generate_ai_explanation", "finalize_result")
    graph.add_edge("finalize_result", END)

    return graph.compile()


def inspect_with_graph(
    transaction: BankingTransaction,
    ollama_client: OllamaClient,
    stream_writer: StreamWriter | None = None,
) -> InspectionResult:
    app = build_inspection_graph(ollama_client, stream_writer)
    final_state = app.invoke({"transaction": transaction})
    result = AgentState.model_validate(final_state).final_result
    if result is None:
        raise RuntimeError("LangGraph workflow completed without a final inspection result.")
    return result


class FakeStreamingOllamaClient:
    """Tiny test helper used by unit tests without network access."""

    def __init__(self, chunks: Iterable[str]) -> None:
        self.chunks = list(chunks)

    def stream_generate(self, prompt: str) -> Iterable[str]:
        return iter(self.chunks)

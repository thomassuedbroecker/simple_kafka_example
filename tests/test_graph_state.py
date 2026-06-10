from banking_ai.graph import (
    FakeStreamingOllamaClient,
    build_explanation_prompt,
    inspect_with_graph,
)
from banking_ai.models import AgentState
from banking_ai.models import BankingTransaction


def test_graph_creates_final_result_without_network() -> None:
    transaction = BankingTransaction.model_validate(
        {
            "transaction_id": "txn-graph",
            "account_id": "acc-graph",
            "amount": 1200,
            "currency": "EUR",
            "merchant": "Local Shop",
            "country": "DE",
            "timestamp": "2026-06-10T10:15:00Z",
            "transaction_type": "card_payment",
        }
    )
    streamed: list[str] = []

    result = inspect_with_graph(
        transaction,
        ollama_client=FakeStreamingOllamaClient(["review ", "large amount"]),
        stream_writer=streamed.append,
    )

    assert result.status == "SUSPICIOUS"
    assert [finding.rule_id for finding in result.findings] == [
        "amount_greater_than_1000"
    ]
    assert result.ai_explanation == "review large amount"
    assert streamed == ["review ", "large amount"]


def test_prompt_tells_model_triggered_rules_are_triggered() -> None:
    transaction = BankingTransaction.model_validate(
        {
            "transaction_id": "txn-prompt",
            "account_id": "acc-prompt",
            "amount": 1200,
            "currency": "EUR",
            "merchant": "Local Shop",
            "country": "DE",
            "timestamp": "2026-06-10T10:15:00Z",
            "transaction_type": "card_payment",
        }
    )
    result = inspect_with_graph(
        transaction,
        ollama_client=FakeStreamingOllamaClient(["explanation"]),
    )

    prompt = build_explanation_prompt(
        AgentState(
            transaction=transaction,
            findings=result.findings,
            suspicious=True,
        )
    )

    assert "amount_greater_than_1000" in prompt
    assert "Do not say that no rule was triggered." in prompt

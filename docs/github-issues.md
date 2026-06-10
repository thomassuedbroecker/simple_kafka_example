# GitHub Issues Backlog

These are GitHub-ready issue definitions. Create them with:

```bash
gh auth login
./scripts/create_github_issues.sh
```

The script checks existing issue titles first and skips issues that already exist.

## GH-001: Add local Kafka broker in KRaft mode

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/1

Labels: `learning`, `kafka`, `infrastructure`

Body:

Create a Docker Compose setup with one local Kafka broker in KRaft mode and no ZooKeeper.

Acceptance criteria:

- `./scripts/start.sh` starts Kafka through Docker Compose.
- `./scripts/stop.sh` stops Kafka.
- Kafka exposes `localhost:9092`.
- The setup is local-only and does not use cloud Kafka.

Traceability: LI-001, LI-008.

## GH-002: Implement demo transaction producer

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/2

Labels: `learning`, `kafka`, `producer`

Body:

Create a Python Kafka producer that sends predefined fake banking transactions to `banking.transactions`.

Acceptance criteria:

- `python -m banking_ai.producer` sends at least 10 transactions.
- Message key is `transaction_id`.
- Message value is a JSON transaction payload.
- The producer prints what it queued and what Kafka acknowledged.

Traceability: LI-002, LI-005.

## GH-003: Implement transaction consumer with manual offset commit

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/3

Labels: `learning`, `kafka`, `consumer`

Body:

Create a Python Kafka consumer that reads transactions, inspects them, and commits offsets only after successful inspection.

Acceptance criteria:

- `python -m banking_ai.consumer --max-messages 10` consumes a bounded demo run.
- The consumer uses the configured consumer group id.
- The consumer starts from earliest messages for a new group.
- Invalid messages are handled clearly.
- Ollama failure does not silently commit the inspected message.

Traceability: LI-003, LI-004, LI-007.

## GH-004: Implement deterministic transaction rules

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/4

Labels: `learning`, `rules`, `testing`

Body:

Implement simple first-pass inspection rules before any LLM explanation is generated.

Acceptance criteria:

- `amount > 1000` is suspicious.
- `country not in ["DE", "NL", "FR", "AT"]` is suspicious.
- `transaction_type == "cash_withdrawal" and amount > 500` is suspicious.
- Merchant names containing `crypto`, `casino`, or `unknown` are suspicious.
- Unit tests cover normal and suspicious examples.

Traceability: LI-004.

## GH-005: Add typed Pydantic models

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/5

Labels: `learning`, `models`, `python`

Body:

Define simple Pydantic v2 models for transactions, rule findings, final inspection results, and LangGraph state.

Acceptance criteria:

- `BankingTransaction` validates the demo JSON event shape.
- `RuleFinding` records rule id, reason, relevant fields, and suspicious flag.
- `InspectionResult` records final status and explanation.
- `AgentState` represents graph workflow state.
- Unit tests cover model validation.

Traceability: LI-005.

## GH-006: Build LangGraph inspection workflow

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/6

Labels: `learning`, `langgraph`, `ai`

Body:

Use a real LangGraph `StateGraph` to organize the inspection as state transitions.

Acceptance criteria:

- The graph has conceptual nodes for `load_transaction`, `apply_rules`, `generate_ai_explanation`, and `finalize_result`.
- The graph combines deterministic findings with the AI explanation.
- A unit test verifies graph behavior without Kafka, Ollama, Docker, or network access.

Traceability: LI-004, LI-006, LI-010.

## GH-007: Add local Ollama streaming client

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/7

Labels: `learning`, `ollama`, `streaming`

Body:

Create a minimal `httpx` client for Ollama `/api/generate` that streams response chunks to the terminal.

Acceptance criteria:

- The client uses `OLLAMA_BASE_URL` and `OLLAMA_MODEL` defaults.
- The client streams chunks progressively.
- Missing Ollama and missing model errors are clear.
- No external AI API, hosted tracing, cloud service, or API key is used.

Traceability: LI-007.

## GH-008: Add beginner-friendly scripts

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/8

Labels: `learning`, `developer-experience`

Body:

Add simple bash scripts for the main learning flow.

Acceptance criteria:

- Scripts use `set -euo pipefail`.
- `scripts/start.sh` starts Kafka.
- `scripts/stop.sh` stops Kafka.
- `scripts/create_topics.sh` creates `banking.transactions`.
- `scripts/produce_demo_transactions.sh` runs the producer.
- `scripts/consume_and_inspect.sh` runs the consumer.

Traceability: LI-001, LI-002, LI-003, LI-008.

## GH-009: Write README learning guide

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/9

Labels: `learning`, `documentation`

Body:

Document the project for a beginner who wants to understand Kafka basics and local AI streaming.

Acceptance criteria:

- README explains what the project is and is not.
- README explains Kafka, Ollama, LangGraph, rules, offsets, and consumer groups.
- README includes the required Mermaid architecture diagram.
- README includes install, run, test, troubleshooting, and learning exercise commands.
- README links to the traceability matrix.

Traceability: LI-009.

## GH-010: Add infrastructure-free unit tests

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/10

Labels: `learning`, `testing`

Body:

Add focused unit tests that verify core behavior without requiring Kafka, Docker, Ollama, or network access.

Acceptance criteria:

- Rule tests cover normal and suspicious transactions.
- Model tests cover validation.
- Graph tests use a fake streaming Ollama client.
- `pytest` passes after installing development dependencies.

Traceability: LI-004, LI-005, LI-006, LI-010.

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

## GH-012: Add MIT license and open-source transparency docs

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/12

Labels: `documentation`

Body:

Add repository-level license and open-source transparency documentation so users understand the project license and third-party dependency/model boundaries.

Acceptance criteria:

- Repository includes an MIT `LICENSE`.
- Python package metadata references the license.
- README links to license and third-party notices.
- Third-party dependencies and local Ollama model licensing boundaries are documented.

Traceability: repository governance and open-source transparency.

Issue [#11](https://github.com/thomassuedbroecker/simple_kafka_example/issues/11) was created as a duplicate of GH-010 and is closed as duplicate.

## GH-013: Improve component license transparency

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/13

Labels: `documentation`

Body:

Add a transparent component-level license inventory for the repository.

Acceptance criteria:

- Document direct Python dependency licenses with versions, license evidence, source links, purpose, and bundled/not-bundled status.
- Document transitive dependencies observed in the local verification environment.
- Document local runtime components such as Apache Kafka container image and Ollama.
- Document local Ollama model licensing boundaries, including `qwen3-coder:30b` and `llama3.2` notes.
- Link the license review to the component inventory.

Traceability: open-source transparency and license due-diligence documentation.

## GH-014: Make demo run fail clearly when Kafka has no messages

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/14

Labels: `developer-experience`

Body:

The README flow can look broken when a learner runs the consumer before producing transactions, or immediately after cleanup recreated Kafka with an empty topic. The consumer waits for messages and librdkafka can also print confusing localhost IPv6 connection-refused startup logs on macOS.

Acceptance criteria:

- Kafka clients prefer IPv4 localhost behavior to reduce macOS `::1` connection-refused noise.
- The consume script has a bounded idle timeout for demos.
- When no messages arrive, the consumer prints a clear hint to run the producer first or use a new consumer group for replay.
- README troubleshooting explains the correct order after cleanup: start Kafka, create topic, produce transactions, then consume.
- Unit tests still pass without Docker, Kafka, Ollama, or network access.

Traceability: LI-003, LI-008, LI-009, LI-010.

## GH-015: Reorder README around objective and expected results

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/15

Labels: `documentation`

Body:

The README currently repeats setup sections and makes the objective harder to see. Reorder the topics so learners first see the objective, expected result, architecture, run flow, cleanup, learning concepts, and then reference material.

Acceptance criteria:

- README has an explicit objective near the top.
- Expected terminal results are visible before reference material.
- Duplicate install/start/produce/consume sections are consolidated or renamed as reference material.
- Kafka and local AI concepts are kept, but placed after the runnable flow.
- Verification, traceability, license, troubleshooting, and learning exercises remain linked.
- Tests and markdown whitespace checks pass.

Traceability: LI-009.

## GH-016: Add optional Kafbat UI to local Kafka learning setup

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/16

Labels: `learning`, `kafka`, `developer-experience`, `documentation`

Body:

Add Kafbat UI as an optional local Kafka web console for the learning project.

Acceptance criteria:

- `docker-compose.yml` starts Kafbat UI alongside the local KRaft Kafka broker.
- Kafka has a host listener for Python clients and an internal listener for Kafbat UI.
- `scripts/start.sh` starts the UI with Kafka.
- README includes Kafbat UI in the run flow as a learning step after producing transactions.
- README explains what to inspect in the UI: topic, messages, partitions, consumer group, and offsets.
- Traceability, project status, GitHub issue docs, and third-party notices mention Kafbat UI.
- Tests and `docker compose config` pass.

Traceability: LI-001, LI-002, LI-003, LI-008, LI-009, LI-011.

## GH-017: Refresh repository sync verification evidence

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/17

Labels: `documentation`

Body:

Refresh repository status and verification evidence after the Kafbat UI integration.

Acceptance criteria:

- Project status date reflects the latest sync verification.
- Verification notes date reflects the latest local checks.
- Verification notes include the current checks: open issue list, `docker compose config`, `pytest`, and `git status`.
- Commit references this issue.

Traceability: documentation/code synchronization.

## GH-018: Document executed test coverage details

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/18

Labels: `documentation`, `testing`

Body:

Add clearer documentation for the tests that were executed during verification.

Acceptance criteria:

- Verification docs list the executed test command and result.
- Verification docs explain which test files ran and what behavior each file validates.
- The Tests workflow has two independent gates: Python unit tests and Docker Compose configuration validation.
- Project status references the test-detail documentation update.
- Commit references this issue.

Traceability: LI-010 and repository verification evidence.

## GH-019: Add README project icon

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/19

Labels: `documentation`

Body:

Add a visible project icon at the top of the README so the repository has a clearer first impression.

Acceptance criteria:

- Add a repo-local icon asset.
- Show the icon at the top of `README.md`.
- Keep the README objective and expected result sections clear.
- Update local issue/status documentation.
- Commit references this issue.

Traceability: README usability and learning-project presentation.

Status: closed as superseded by GH-020 after the request was clarified as a test execution status badge.

## GH-020: Add README test execution status badge

GitHub issue: https://github.com/thomassuedbroecker/simple_kafka_example/issues/20

Labels: `documentation`, `testing`

Body:

Add a visible test execution status badge at the top of `README.md` for the Tests workflow.

Acceptance criteria:

- README top shows the GitHub Actions Tests workflow badge.
- Badge links to `.github/workflows/tests.yml` workflow runs.
- Documentation clarifies that the workflow has two independent gates: Python unit tests and Docker Compose configuration validation.
- Local issue/status docs are updated.
- Commit references this issue.

Traceability: test execution status visibility and verification evidence.

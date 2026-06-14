# Traceability Matrix

This matrix connects the learning intent to requirements, implementation files, tests, and GitHub issues.

| ID | Learning Intent / Requirement | Implementation | Tests / Verification | GitHub Issue |
| --- | --- | --- | --- | --- |
| LI-001 | Teach Kafka topic basics with one named stream, `banking.transactions`. | `docker-compose.yml`, `src/banking_ai/config.py`, `src/banking_ai/kafka_admin.py`, `scripts/create_topics.sh` | `./scripts/start.sh`, `./scripts/create_topics.sh` | [#1](https://github.com/thomassuedbroecker/simple_kafka_example/issues/1) |
| LI-002 | Teach Kafka producer basics with JSON message values and `transaction_id` message keys. | `src/banking_ai/producer.py`, `src/banking_ai/models.py` | `python -m banking_ai.producer` | [#2](https://github.com/thomassuedbroecker/simple_kafka_example/issues/2) |
| LI-003 | Teach Kafka consumer group and offset basics. | `src/banking_ai/consumer.py`, `src/banking_ai/config.py` | `python -m banking_ai.consumer --max-messages 10` | [#3](https://github.com/thomassuedbroecker/simple_kafka_example/issues/3) |
| LI-004 | Inspect transactions with deterministic rules before LLM explanation. | `src/banking_ai/rules.py`, `src/banking_ai/graph.py`, `src/banking_ai/consumer.py` | `tests/test_rules.py`, `pytest` | [#4](https://github.com/thomassuedbroecker/simple_kafka_example/issues/4) |
| LI-005 | Use typed, beginner-readable models for events, findings, results, and graph state. | `src/banking_ai/models.py` | `tests/test_models.py` | [#5](https://github.com/thomassuedbroecker/simple_kafka_example/issues/5) |
| LI-006 | Use a real LangGraph `StateGraph` to show state movement through inspection steps. | `src/banking_ai/graph.py` | `tests/test_graph_state.py` | [#6](https://github.com/thomassuedbroecker/simple_kafka_example/issues/6) |
| LI-007 | Use local-only Ollama through direct HTTP API calls and stream output to the terminal. | `src/banking_ai/ollama_client.py`, `src/banking_ai/consumer.py` | Manual: `ollama serve`, `ollama pull llama3.2`, consumer run | [#7](https://github.com/thomassuedbroecker/simple_kafka_example/issues/7) |
| LI-008 | Keep local container startup and shutdown simple for macOS M3 learners. | `docker-compose.yml`, `scripts/start.sh`, `scripts/stop.sh` | `./scripts/start.sh`, `./scripts/stop.sh` | [#8](https://github.com/thomassuedbroecker/simple_kafka_example/issues/8) |
| LI-009 | Provide clear beginner documentation explaining why each part exists. | `README.md`, `.env.example`, `docs/traceability.md` | Documentation review against README checklist | [#9](https://github.com/thomassuedbroecker/simple_kafka_example/issues/9) |
| LI-010 | Keep tests focused and independent from Kafka, Docker, Ollama, and network access. | `tests/test_rules.py`, `tests/test_models.py`, `tests/test_graph_state.py` | `pytest` | [#10](https://github.com/thomassuedbroecker/simple_kafka_example/issues/10) |
| LI-011 | Use Kafbat UI to visually inspect topics, messages, consumer groups, partitions, and offsets. | `docker-compose.yml`, `scripts/start.sh`, `README.md` | `docker compose config`, manual: open `http://localhost:8080` | [#16](https://github.com/thomassuedbroecker/simple_kafka_example/issues/16) |

## Forward Traceability

- Kafka learning goals map to `docker-compose.yml`, `kafka_admin.py`, `producer.py`, and `consumer.py`.
- Kafka UI visibility maps to `docker-compose.yml`, `scripts/start.sh`, and the Kafbat UI learning step in the README.
- Rule-learning goals map to `rules.py` and `tests/test_rules.py`.
- LangGraph-learning goals map to `graph.py` and `tests/test_graph_state.py`.
- Local AI streaming goals map to `ollama_client.py` and the streaming callback in `consumer.py`.
- Beginner-readability goals map to the README, small modules, and focused scripts.

## Backward Traceability

- `producer.py` exists to satisfy LI-002.
- `consumer.py` exists to satisfy LI-003, LI-004, and LI-007.
- `graph.py` exists to satisfy LI-006 and connect LI-004 with LI-007.
- `ollama_client.py` exists to satisfy LI-007 without external AI APIs.
- `tests/` exists to satisfy LI-010 and verify core behavior without infrastructure.
- The Kafbat UI service exists to satisfy LI-011 without changing the core terminal-first producer and consumer flow.

## Issue To Code Index

- [#1](https://github.com/thomassuedbroecker/simple_kafka_example/issues/1): `docker-compose.yml`, `src/banking_ai/kafka_admin.py`, `scripts/start.sh`, `scripts/create_topics.sh`
- [#2](https://github.com/thomassuedbroecker/simple_kafka_example/issues/2): `src/banking_ai/producer.py`, `src/banking_ai/models.py`
- [#3](https://github.com/thomassuedbroecker/simple_kafka_example/issues/3): `src/banking_ai/consumer.py`, `src/banking_ai/config.py`
- [#4](https://github.com/thomassuedbroecker/simple_kafka_example/issues/4): `src/banking_ai/rules.py`, `src/banking_ai/graph.py`, `tests/test_rules.py`
- [#5](https://github.com/thomassuedbroecker/simple_kafka_example/issues/5): `src/banking_ai/models.py`, `tests/test_models.py`
- [#6](https://github.com/thomassuedbroecker/simple_kafka_example/issues/6): `src/banking_ai/graph.py`, `tests/test_graph_state.py`
- [#7](https://github.com/thomassuedbroecker/simple_kafka_example/issues/7): `src/banking_ai/ollama_client.py`, `src/banking_ai/consumer.py`
- [#8](https://github.com/thomassuedbroecker/simple_kafka_example/issues/8): `scripts/start.sh`, `scripts/stop.sh`, `scripts/produce_demo_transactions.sh`, `scripts/consume_and_inspect.sh`
- [#9](https://github.com/thomassuedbroecker/simple_kafka_example/issues/9): `README.md`, `.env.example`, `docs/traceability.md`, `docs/github-issues.md`
- [#10](https://github.com/thomassuedbroecker/simple_kafka_example/issues/10): `tests/test_rules.py`, `tests/test_models.py`, `tests/test_graph_state.py`
- [#16](https://github.com/thomassuedbroecker/simple_kafka_example/issues/16): `docker-compose.yml`, `scripts/start.sh`, `README.md`

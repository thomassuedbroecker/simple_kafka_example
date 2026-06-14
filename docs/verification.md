# Verification Notes

Date: 2026-06-14

Local container runner: Rancher Desktop with Docker context `rancher-desktop`.

## Verified Commands

Repository sync status:

```bash
git status -sb
gh issue list --state open --limit 50 --json number,title,state,url
```

Result:

```text
## main...origin/main
[]
```

Python unit tests:

```bash
.venv/bin/python -m pytest
```

Result:

```text
12 passed
```

Executed test details:

| Test file | Test cases | What was verified | Infrastructure needed |
| --- | --- | --- | --- |
| `tests/test_config.py` | `test_kafka_base_config_uses_ipv4_for_local_mac_demo` | Shared Kafka client config uses `localhost:9092` and forces IPv4 for the local macOS container setup. | None |
| `tests/test_graph_state.py` | `test_graph_creates_final_result_without_network`, `test_prompt_tells_model_triggered_rules_are_triggered` | LangGraph creates a final inspection result, streams fake Ollama chunks, preserves triggered rule findings, and prompts the model consistently. | None |
| `tests/test_models.py` | `test_transaction_model_accepts_valid_transaction`, `test_transaction_model_rejects_negative_amount` | Pydantic validates valid banking transactions and rejects invalid negative amounts. | None |
| `tests/test_rules.py` | `test_normal_transaction_has_no_findings`, `test_large_amount_is_suspicious`, `test_foreign_country_is_suspicious`, `test_large_cash_withdrawal_is_suspicious`, `test_suspicious_merchant_keyword_is_suspicious` | Deterministic rules correctly classify normal transactions and each suspicious rule trigger. | None |
| `tests/test_results_ui.py` | `test_results_ui_finds_demo_transaction`, `test_results_ui_rejects_unknown_transaction` | Results UI helper finds predefined demo transactions and rejects unknown ids without starting the web server. | None |

The [Tests workflow](../.github/workflows/tests.yml) runs two independent gates:

| Gate | Command | Purpose |
| --- | --- | --- |
| Python unit tests | `python -m pytest` | Runs the 12 infrastructure-free tests listed above. |
| Docker Compose configuration | `docker compose config` | Validates the Kafka plus Kafbat UI Compose file without starting the containers. |

Kafka startup with Rancher Desktop:

```bash
./scripts/start.sh
```

Result:

```text
Container local-kafka-langgraph-banking-ai-kafka Started
Kafka Server started
```

Topic creation:

```bash
PYTHON=.venv/bin/python ./scripts/create_topics.sh
```

Result:

```text
Created topic: banking.transactions
```

Docker Compose configuration with Kafbat UI:

```bash
docker compose config
```

Result:

```text
kafbat-ui:
  image: ghcr.io/kafbat/kafka-ui:latest
  ports:
    - "8080:8080"
kafka:
  KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,INTERNAL://kafka:29092
```

Results UI smoke test:

```bash
.venv/bin/python -m banking_ai.results_ui
curl -fsS http://127.0.0.1:8081/
curl -fsS http://127.0.0.1:8081/api/transactions
```

Result:

```text
Results UI: http://127.0.0.1:8081
HTML page returned
10 demo transactions returned as JSON
```

Producer:

```bash
PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh
```

Result:

```text
Produced 10 demo transactions.
Sent key=txn-1001 topic=banking.transactions partition=0 offset=0
...
Sent key=txn-1010 topic=banking.transactions partition=0 offset=9
```

Consumer and local AI streaming with the installed qwen 30B model:

```bash
PYTHON=.venv/bin/python \
OLLAMA_MODEL=qwen3-coder:30b \
CONSUMER_GROUP_ID=banking-ai-inspector-qwen30b \
MAX_MESSAGES=1 \
./scripts/consume_and_inspect.sh
```

Result:

```text
Received transaction: txn-1001
Rule findings:
- none
AI inspection:
...
Final result:
NORMAL
```

Earlier full 10-message consumer verification was also completed with the already-installed local model `granite4:350m-h`:

```bash
PYTHON=.venv/bin/python \
OLLAMA_MODEL=granite4:350m-h \
CONSUMER_GROUP_ID=banking-ai-inspector-verify \
./scripts/consume_and_inspect.sh
```

Result:

```text
Received transaction: txn-1010
Rule findings:
- amount_greater_than_1000
- foreign_country
- suspicious_merchant_keyword
AI inspection:
...
Final result:
SUSPICIOUS
```

## Notes

- Rancher Desktop worked as the local container runner.
- Kafka ran in one local container in KRaft mode.
- Kafbat UI is configured as an optional local Kafka browser on `http://localhost:8080`.
- Results UI is configured as an optional local browser page on `http://127.0.0.1:8081`.
- Kafka exposes `localhost:9092` for Python clients and `kafka:29092` for Kafbat UI inside the Docker Compose network.
- The Kafka topic `banking.transactions` was created.
- The producer wrote 10 JSON transaction messages using `transaction_id` as the Kafka key.
- The consumer read and inspected 10 messages.
- Deterministic rules flagged suspicious transactions before the LLM explanation.
- Ollama streaming worked with the installed qwen 30B model `qwen3-coder:30b` for a smoke test.
- Ollama streaming also worked for a full 10-message run with the already-installed local model `granite4:350m-h`.
- The default README and code model is `qwen3-coder:30b`, matching the local smoke verification model.
- The scripts now support `PYTHON=.venv/bin/python` and default to `python3` when `PYTHON` is not set, which is more reliable on macOS systems without a `python` executable.
- The consumer script now applies a demo idle timeout through `IDLE_TIMEOUT_SECONDS` and prints a clear producer/replay hint if no messages arrive.
- The Results UI reuses the same rules, LangGraph workflow, and Ollama client as the terminal consumer.

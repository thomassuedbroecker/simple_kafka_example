# Verification Notes

Date: 2026-06-10

Local container runner: Rancher Desktop with Docker context `rancher-desktop`.

## Verified Commands

Python unit tests:

```bash
.venv/bin/python -m pytest
```

Result:

```text
10 passed
```

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
- Kafka exposes `localhost:9092` for Python clients and `kafka:29092` for Kafbat UI inside the Docker Compose network.
- The Kafka topic `banking.transactions` was created.
- The producer wrote 10 JSON transaction messages using `transaction_id` as the Kafka key.
- The consumer read and inspected 10 messages.
- Deterministic rules flagged suspicious transactions before the LLM explanation.
- Ollama streaming worked with the installed qwen 30B model `qwen3-coder:30b` for a smoke test.
- Ollama streaming also worked for a full 10-message run with the already-installed local model `granite4:350m-h`.
- The default README model remains `llama3.2`, but it was not present in `ollama list` during this verification run.
- The scripts now support `PYTHON=.venv/bin/python` and default to `python3` when `PYTHON` is not set, which is more reliable on macOS systems without a `python` executable.
- The consumer script now applies a demo idle timeout through `IDLE_TIMEOUT_SECONDS` and prints a clear producer/replay hint if no messages arrive.

# Local Kafka + LangGraph Banking AI

> Note: this repository is supported and primarily developed with AI assistance from Codex, Copilot, Claude AI, and IBM Bob.

[![Tests](https://github.com/thomassuedbroecker/simple_kafka_example/actions/workflows/tests.yml/badge.svg)](https://github.com/thomassuedbroecker/simple_kafka_example/actions/workflows/tests.yml)

This is a small local-first learning project for macOS on Apple Silicon. It shows how a Python producer writes fake banking transactions into Kafka, how a consumer reads them back, how deterministic inspection rules run first, and how a small LangGraph workflow streams a local Ollama explanation to the terminal and the local Results UI.

## What This Is Not

This project is for learning. It is **not**:

- a production banking system, fraud engine, or security reference architecture
- a scalable or multi-broker Kafka deployment
- a Kubernetes project (Kubernetes is out of scope; see [ADR 0004](docs/adr/0004-no-kubernetes.md))
- a user of any external or cloud AI API
- a user of real banking data

## Local Runtime Requirements

- macOS Apple Silicon.
- **Rancher Desktop is used only as the local container runtime.** Kubernetes is
  not used and should be disabled in Rancher Desktop. The project uses
  `docker compose` commands through Rancher Desktop. Any Docker-compatible
  runtime (Docker Desktop, Colima) also works.
- Ollama installed and running locally on macOS. No external AI API or API key
  is required.
- Python 3.12+.

See [docs/local-execution.md](docs/local-execution.md) for the full local setup,
and [docs/troubleshooting.md](docs/troubleshooting.md) if something fails.

## Objective

Run one complete local example and understand this flow:

```text
producer -> Kafka topic -> consumer -> rules -> LangGraph -> Ollama -> streamed terminal output
```

By the end, you should be able to explain:

- Kafka topic, producer, consumer, message key, message value, consumer group, offset, and JSON payload basics.
- How Kafbat UI can show the topic, messages, consumer group, and offsets visually.
- How the local Results UI shows the selected Kafka topic event, deterministic findings, AI agent steps, and streamed AI explanation text.
- Why deterministic transaction rules run before the LLM explanation.
- How LangGraph moves inspection state through small workflow nodes.
- Where Ollama streams local AI output in the terminal and browser.
- Why this project does not need external AI APIs, cloud services, or API keys.

## Expected Result

After setup, the important successful output is:

```text
Produced 10 demo transactions.

Received transaction: txn-1001

Rule findings:
- none

AI inspection:
This transaction looks normal because ...

Final result:
NORMAL
```

Suspicious transactions should show triggered rules before the AI explanation:

```text
Received transaction: txn-1010

Rule findings:
- amount_greater_than_1000
- foreign_country
- suspicious_merchant_keyword

AI inspection:
This transaction should be reviewed because ...

Final result:
SUSPICIOUS
```

## Architecture

```mermaid
flowchart LR
    A[Demo Transaction Producer] --> B[Kafka Topic: banking.transactions]
    B --> H[Kafbat UI: optional topic browser]
    B --> C[Kafka Consumer: terminal]
    C --> D[Deterministic Rules]
    D --> E[LangGraph Agent]
    E --> F[Ollama Local LLM]
    F --> G[Streamed Terminal Explanation]
    B --> I[Results UI: live consumer or demo replay]
    I --> D
    F --> J[Results UI: streamed AI agent result]
```

Both the terminal consumer and the Results UI's "Consume next from Kafka" mode
read the same topic with a Kafka consumer group and commit offsets. The Results
UI also offers a demo-replay mode that inspects a predefined event from memory
without a broker.

## Demo GIFs

The GIF below shows the local browser UI for inspecting Kafka learning data:

![Kafbat UI and local inspection flow](images/kafbat-ui-1ß.gif)

The GIF below show how to inspect transactions with an AI agent.

![Example inspection of the transactions](images/inspect-transactions.gif)

## Fast Path

For experienced users who just want to run it. Each step is explained in detail
in the next section. Start Rancher Desktop first (Kubernetes disabled).

```bash
# 1. Create and activate a Python environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install the project
pip install -e ".[dev]"

# 3. Start Ollama locally (in its own terminal)
ollama serve

# 4. Pull the local model
ollama pull qwen3-coder:30b

# 5. Start Kafka locally with Rancher Desktop containers
./scripts/start.sh

# 6. Create the Kafka topic
PYTHON=.venv/bin/python ./scripts/create_topics.sh

# 7. Produce demo transactions
PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh

# 8. Consume and inspect transactions
PYTHON=.venv/bin/python MAX_MESSAGES=10 ./scripts/consume_and_inspect.sh
```

Or run the whole happy-path demo in one transparent step:

```bash
PYTHON=.venv/bin/python ./scripts/demo.sh
```

The required learning path is:

```text
Producer -> Kafka -> Consumer -> Rules -> LangGraph -> Ollama -> Terminal
```

Kafbat UI and the Results UI are optional visibility tools, not part of the
required path.

## Run The Example

Use this order from a clean checkout. If you run the consumer before producing transactions, there is nothing to inspect.

### 1. Install Dependencies

What you learn: Python project dependencies should be isolated in a disposable virtual environment. Official resource: [Python `venv` documentation](https://docs.python.org/3/library/venv.html).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Start Kafka And Kafbat UI

Start your local container runner first, such as Rancher Desktop, Docker Desktop, or Colima.

What you learn: Kafka runs as a local container in this project, Docker Compose starts the broker, and Kafbat UI gives you a visual read-only way to inspect the learning flow. Official resources: [Docker Compose documentation](https://docs.docker.com/compose/), [Apache Kafka quickstart](https://kafka.apache.org/quickstart/), and [Kafbat UI documentation](https://ui.docs.kafbat.io/).

```bash
./scripts/start.sh
sleep 10
PYTHON=.venv/bin/python ./scripts/create_topics.sh
```

Expected result:

```text
Container local-kafka-langgraph-banking-ai-kafka Running
Container local-kafka-langgraph-banking-ai-kafbat-ui Running
Created topic: banking.transactions
```

or:

```text
Topic already exists: banking.transactions
```

The Kafka broker runs in KRaft mode, which means there is no ZooKeeper container.

Open Kafbat UI at:

```text
http://localhost:8080
```

Expected UI result: a cluster named `local-kafka`.

### 3. Start Ollama

Install Ollama from https://ollama.com if it is not installed yet.

What you learn: Ollama runs the LLM locally and exposes a local HTTP API, so the inspection explanation does not call an external AI service. Official resources: [Ollama API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md) and [Ollama model library](https://ollama.com/library).

In one terminal:

```bash
ollama serve
```

In another terminal, pull the default local model:

```bash
ollama pull qwen3-coder:30b
export OLLAMA_MODEL=qwen3-coder:30b
```

Verify Ollama is reachable and the model is present:

```bash
ollama list
curl http://localhost:11434/api/tags
```

`qwen3-coder:30b` is the default. It explains well but needs more local
resources. If you have limited resources, override `OLLAMA_MODEL` with a smaller
local model of your choice.

### 4. Produce Demo Transactions

What you learn: a Kafka producer writes a JSON message value to a topic and uses `transaction_id` as the message key.

```bash
PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh
```

Expected result:

```text
Queued transaction txn-1001: {...}
...
Sent key=txn-1010 topic=banking.transactions partition=0 offset=9
Produced 10 demo transactions.
```

### 5. Inspect Kafka In Kafbat UI

What you learn: Kafka messages remain in the topic, and a UI can help you connect the terminal commands to Kafka concepts.

Open:

```text
http://localhost:8080
```

Look for:

- Cluster: `local-kafka`
- Topic: `banking.transactions`
- Messages: JSON transaction payloads
- Key: `transaction_id`, such as `txn-1001`
- Partition: `0` in this single-partition learning setup

After running the consumer in the next step, also inspect:

- Consumer group: `banking-ai-inspector`
- Offsets: the committed position after inspected messages

Kafbat UI is only for learning visibility here. The application still works from the terminal without using the UI.

### 6. Consume And Inspect Transactions

What you learn: a Kafka consumer reads messages as part of a consumer group, the app applies deterministic rules first, LangGraph moves state through the inspection workflow, and Ollama streams explanation text back to the terminal. Official resource: [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview).

```bash
PYTHON=.venv/bin/python MAX_MESSAGES=10 ./scripts/consume_and_inspect.sh
```

Expected normal transaction output:

```text
Consuming from topic 'banking.transactions' with group 'banking-ai-inspector'.

Received transaction: txn-1001

Rule findings:
- none

AI inspection:
This transaction looks normal because ...

Final result:
NORMAL
Reviewer check: No deterministic rule was triggered; spot-check normal account context if needed.
```

Expected suspicious transaction output:

```text
Received transaction: txn-1010

Rule findings:
- amount_greater_than_1000
- foreign_country
- suspicious_merchant_keyword

AI inspection:
This transaction should be reviewed because ...

Final result:
SUSPICIOUS
Reviewer check: Review the triggered rule fields and compare the transaction with normal customer behavior.
```

If no messages arrive, the script stops after the demo idle timeout:

```text
No Kafka messages arrived within 30 seconds.
Run the producer first with: PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh
If you already consumed these messages, use a new CONSUMER_GROUP_ID to replay them.
```

### 7. Open The Results UI

What you learn: Kafbat UI shows Kafka internals, while this small project UI shows the selected Kafka topic event and the AI agent result in one browser page.

Start the local results UI:

```bash
PYTHON=.venv/bin/python ./scripts/start_results_ui.sh
```

Open:

```text
http://127.0.0.1:8081
```

Expected result:

```text
Results UI: http://127.0.0.1:8081
Press Ctrl+C to stop.
```

The UI has two modes:

- **Consume next from Kafka** (needs the broker running and produced messages):
  reads the next live message from `banking.transactions` using the consumer
  group `banking-ai-inspector`, shows the partition and offset, inspects it, and
  commits the offset only after a successful inspection. Click it again to read
  the next message and watch the offset advance. To replay, change
  `CONSUMER_GROUP_ID` before starting the UI.
- **Inspect selected (demo replay)**: inspects the event chosen in the dropdown
  from memory, without a broker. Useful when Kafka is not running.

In both modes you see:

- The topic name, message key, and JSON message value (plus group, partition,
  and offset in live consume mode).
- The AI agent workflow steps. Live consume shows `consume_from_kafka` first,
  then `load_transaction`, `apply_rules`, `generate_ai_explanation`, and
  `finalize_result`. Demo replay skips `consume_from_kafka`.
- The AI explanation streaming into the page.
- The difference between normal and suspicious transactions.

This UI reuses the same deterministic rules, LangGraph workflow, and Ollama client as the terminal consumer. It does not replace Kafka or Kafbat UI; it focuses on connecting one topic event to the AI agent inspection result.

### 8. Run Tests

What you learn: the rule logic, model validation, Kafka config, Results UI event helpers, and graph state behavior can be verified without Kafka, containers, Ollama, or network access. Official resource: [pytest documentation](https://docs.pytest.org/en/stable/).

```bash
.venv/bin/python -m pytest
```

Expected result:

```text
16 passed
```

The [Tests workflow](.github/workflows/tests.yml) runs two independent gates:

| Gate | Command | What it proves |
| --- | --- | --- |
| Python unit tests | `python -m pytest` | Rules, Pydantic models, LangGraph state flow, fake Ollama streaming, local Kafka client config, and Results UI topic-event helpers work without Docker, Kafka, Ollama, or network access. |
| Docker Compose configuration | `docker compose config` | The Kafka and Kafbat UI Compose configuration is syntactically valid and renders the intended services, ports, and listener settings. |

## Clean Up

Stop and remove the local Kafka container and Docker Compose network:

```bash
./scripts/stop.sh
```

Stop `ollama serve` with `Ctrl+C` in the terminal where it is running.

Remove the Python virtual environment if you want a fully clean local checkout:

```bash
deactivate
rm -rf .venv
```

Optional Docker image cleanup if you want to reclaim disk space:

```bash
docker rmi apache/kafka:3.8.1
```

This project does not define a persistent Kafka volume. After `./scripts/stop.sh`, the topic is empty until you start Kafka and produce transactions again.

## Learning Concepts

### Why These Parts Exist

- Kafka teaches event streaming: a producer writes events into a named topic, and a consumer reads those events later.
- Kafbat UI helps you see the topic, messages, consumer group, partitions, and offsets while learning.
- Results UI helps you inspect the selected topic event, AI agent steps, final rule output, and AI output in a browser.
- Ollama runs an LLM locally without API keys, cloud services, or external AI APIs.
- LangGraph makes the inspection flow explicit as small state transitions.
- Deterministic rules run before the LLM because important decisions should not depend only on generated text. Each rule returns a structured `RuleFinding` with `rule_id`, `severity` (`low`, `medium`, or `high`), `reason`, and `relevant_fields`, so the result is easy to read and test. See [ADR 0002](docs/adr/0002-deterministic-rules-before-llm.md).

### Kafka Basics In This Project

- Topic: `banking.transactions` is the named stream of transaction events.
- Producer: `python -m banking_ai.producer` writes JSON transaction events into Kafka.
- Message key: the producer uses `transaction_id` as the Kafka key so related messages can be identified consistently.
- Message value: the transaction payload is serialized as JSON.
- Consumer: `python -m banking_ai.consumer` reads events from the topic.
- Consumer group: `banking-ai-inspector` lets Kafka coordinate which consumer instance reads which messages.
- Offset: Kafka tracks each consumer group's position in the topic. This example commits an offset only after a transaction was inspected successfully.
- Kafbat UI: `http://localhost:8080` shows the local Kafka cluster, topic, messages, consumer group, and offsets.
- Results UI: `http://127.0.0.1:8081` can consume the next live message with a Kafka consumer group (showing partition and offset) or replay a predefined demo event, then shows the AI agent steps, rule findings, final status, reviewer check, and streamed AI explanation.

### Offsets And Consumer Groups

The consumer uses the group id `banking-ai-inspector`. Kafka stores the group's offset, which is the position of the next message the group should read.

This example disables automatic offset commits and commits manually after a transaction has been inspected. That keeps the learning point clear: the offset is advanced only after the work for a message succeeds.

If you run the same consumer group again after all messages were committed, it may not read old messages. To replay from the beginning while learning, change `CONSUMER_GROUP_ID` to a new value:

```bash
export CONSUMER_GROUP_ID=banking-ai-inspector-run-2
python -m banking_ai.consumer --max-messages 10 --idle-timeout-seconds 30
```

### Local AI Basics

Ollama runs the model on your machine. The consumer calls the local Ollama HTTP API at `http://localhost:11434/api/generate` and prints streamed text chunks as they arrive.

No OpenAI, Anthropic, Gemini, hosted LangSmith, hosted vector database, cloud Kafka, or API key is used.

Ollama models are not bundled with this repository. Check the license for any model you pull locally, such as `qwen3-coder:30b`, before redistributing model files or outputs in another project.

## Configuration

Defaults are local and beginner-friendly:

```bash
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TRANSACTION_TOPIC=banking.transactions
INSPECTION_TOPIC=banking.transaction.inspections
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3-coder:30b
CONSUMER_GROUP_ID=banking-ai-inspector
```

Kafbat UI is configured in Docker Compose with:

```bash
KAFKA_CLUSTERS_0_NAME=local-kafka
KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:29092
```

Copy `.env.example` if you want a local reference file. The Python code reads environment variables directly.

The Python helper scripts use `${PYTHON:-python3}`. If your virtual environment is not activated, prefix them with `PYTHON=.venv/bin/python`.

The Results UI is a local Python process started with `scripts/start_results_ui.sh`; it is not a container and does not call external AI APIs. It renders the selected demo transaction as the Kafka topic event that the producer sends: topic `banking.transactions`, key `transaction_id`, and JSON message value.

## Documentation And Traceability

Traceability from learning intent to code is maintained in [docs/traceability.md](docs/traceability.md). GitHub issue definitions and links for the main work topics are in [docs/github-issues.md](docs/github-issues.md). Runtime verification notes are in [docs/verification.md](docs/verification.md), and issue completion status is summarized in [docs/project-status.md](docs/project-status.md).

Local setup and operations are documented in [docs/local-execution.md](docs/local-execution.md) and [docs/troubleshooting.md](docs/troubleshooting.md). Key design decisions are recorded as ADRs in [docs/adr/](docs/adr/): local-first with Rancher Desktop ([0001](docs/adr/0001-local-first-rancher-desktop.md)), deterministic rules before the LLM ([0002](docs/adr/0002-deterministic-rules-before-llm.md)), Kafka learning scope ([0003](docs/adr/0003-kafka-learning-scope.md)), and no Kubernetes ([0004](docs/adr/0004-no-kubernetes.md)).

License transparency is documented in [LICENSE](LICENSE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and [docs/license-review.md](docs/license-review.md). The project code is MIT licensed.

## Troubleshooting

Quick reference matrix (full version in [docs/troubleshooting.md](docs/troubleshooting.md)):

| Problem | Check | Likely fix |
| --- | --- | --- |
| Docker command not found | `docker version` | Enable the Docker-compatible runtime in Rancher Desktop |
| Kafka not reachable | `docker compose ps` | Start containers with `./scripts/start.sh` |
| Kafbat UI not reachable | open `http://localhost:8080` | Check `docker compose logs kafbat-ui` |
| No messages consumed | change `CONSUMER_GROUP_ID` | Existing offsets were already committed; use a new group to replay |
| Ollama not reachable | `curl http://localhost:11434/api/tags` | Start `ollama serve` |
| Ollama model missing | `ollama list` | Run `ollama pull qwen3-coder:30b` |
| Python import error | `pip install -e ".[dev]"` | Reinstall the package into your virtual environment |
| Tests fail | `./scripts/verify.sh` | Fix the syntax, Compose, or test errors it reports |

Kafka is not reachable:

```bash
./scripts/start.sh
PYTHON=.venv/bin/python ./scripts/create_topics.sh
```

Check that your local container runner is running and that port `9092` is free.

Kafbat UI is not reachable:

```bash
docker compose ps
docker compose logs kafbat-ui
```

Check that port `8080` is free and open `http://localhost:8080`.

Results UI is not reachable:

```bash
PYTHON=.venv/bin/python ./scripts/start_results_ui.sh
```

Check that port `8081` is free and open `http://127.0.0.1:8081`.

Ollama is not reachable:

```bash
ollama serve
```

Model is missing:

```bash
ollama pull qwen3-coder:30b
```

Consumer reads no messages:

- Make sure you ran `PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh` after the most recent `./scripts/start.sh`.
- The messages may already be committed for the current consumer group.
- Try a new group id with `export CONSUMER_GROUP_ID=banking-ai-inspector-run-2`.
- Produce demo transactions again.

Python cannot import `banking_ai`:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

## Learning Exercises

- Add the optional topic `banking.transaction.inspections` and publish final inspection results to it.
- Add one more deterministic rule and a unit test for it.
- Change `CONSUMER_GROUP_ID` and observe how offset behavior changes.
- Add another consumer in the same group and observe how Kafka coordinates reads.
- Extend the LangGraph state with a reviewer note.
- Compare two local Ollama models and observe speed and explanation differences.
- Extend the Results UI to read inspected records from the optional `banking.transaction.inspections` topic.

## Local Privacy Note

This project runs locally. Kafka runs in local containers using Rancher Desktop.
Ollama runs locally on macOS. No external AI API is required. No API keys are
required. No real banking data should be used. The project is for learning only.
This is not a claim of production-grade privacy, security, or compliance.

## Known Limitations

- Single Kafka broker, single partition, KRaft mode. Not a scalable or
  multi-broker deployment.
- Deterministic rules are intentionally simple teaching examples, not real fraud
  detection.
- The LLM only explains the rule-based decision; it does not decide the status.
- No persistent Kafka volume: stopping containers clears the topic.
- Out of scope: Kubernetes, cloud AI APIs, real banking data, authentication,
  real databases, and distributed deployment. See
  [docs/project-status.md](docs/project-status.md).

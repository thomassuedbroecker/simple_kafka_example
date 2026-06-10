You are a senior Python developer and software architect.

Build a small local-first learning project for macOS M3.

# Objective

Create a very simple but structured example application to learn Kafka basics and combine them with local AI streaming.

The application must demonstrate:

1. Basic Kafka concepts
   - topic
   - producer
   - consumer
   - message key
   - message value
   - consumer group
   - offset basics
   - JSON event payloads

2. A simple banking transaction inspection use case
   - Generate simple banking transaction events.
   - Send them to Kafka.
   - Consume them from Kafka.
   - Inspect them with a local LangGraph agent.
   - Stream the AI inspection result back to the terminal.

3. Local-only AI execution
   - Use Ollama running locally.
   - Do not call external AI APIs.
   - Do not use cloud services.
   - Do not require API keys.

# Target Environment

The target machine is:

- macOS on Apple Silicon M3
- Local development only
- Python as programming language
- Containers running locally
- Ollama as local inference runtime
- Kafka running in local containers

Use Docker or Podman-compatible container setup.
Prefer Docker Compose syntax unless there is a strong reason not to.

# Important Naming Clarification

The user wrote “ranker for the containers”.
Interpret this as “runner for the containers”.
Use local container runtime wording in the documentation.

# Core Stack

Use:

- Python 3.12+
- Apache Kafka in a local container
- confluent-kafka Python client
- LangGraph
- Ollama
- Local LLM model via Ollama, for example:
  - llama3.2
  - mistral
  - gemma3
  - or another small local model suitable for macOS M3

Do not use:

- OpenAI API
- Anthropic API
- Gemini API
- hosted LangSmith
- hosted vector databases
- cloud Kafka
- authentication
- real banking data
- production security complexity

# Learning Scope

Keep the implementation intentionally simple.

This is not a production banking system.
This is a local learning example.

The application should explain the flow clearly:

transaction producer
    -> Kafka topic
    -> transaction consumer
    -> LangGraph inspection agent
    -> streamed terminal output

# Use Case

Create fake banking transaction events.

Example transaction event:

{
  "transaction_id": "txn-1001",
  "account_id": "acc-001",
  "amount": 249.99,
  "currency": "EUR",
  "merchant": "Online Electronics Store",
  "country": "DE",
  "timestamp": "2026-06-10T10:15:00Z",
  "transaction_type": "card_payment"
}

The LangGraph agent should inspect each transaction and return a simple analysis:

- Is the transaction normal or suspicious?
- Why?
- Which fields were relevant?
- Which simple rule was triggered?
- What should a human reviewer check?

Use simple deterministic rules before calling the LLM.

Example rules:

- amount > 1000 -> suspicious
- country not in ["DE", "NL", "FR", "AT"] -> suspicious
- transaction_type == "cash_withdrawal" and amount > 500 -> suspicious
- merchant contains words like "crypto", "casino", "unknown" -> suspicious

The LangGraph agent should combine:

1. deterministic rule result
2. local LLM explanation via Ollama
3. streamed output to the terminal

# Required Architecture

Create this project structure:

local-kafka-langgraph-banking-ai/
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── src/
│   └── banking_ai/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── kafka_admin.py
│       ├── producer.py
│       ├── consumer.py
│       ├── rules.py
│       ├── ollama_client.py
│       ├── graph.py
│       └── cli.py
├── scripts/
│   ├── start.sh
│   ├── stop.sh
│   ├── create_topics.sh
│   ├── produce_demo_transactions.sh
│   └── consume_and_inspect.sh
└── tests/
    ├── test_rules.py
    ├── test_models.py
    └── test_graph_state.py

# Kafka Requirements

Create a local Kafka setup with:

- one Kafka broker
- one transaction topic
- topic name: banking.transactions
- optional second topic: banking.transaction.inspections

Kafka should be easy to start with:

./scripts/start.sh

And easy to stop with:

./scripts/stop.sh

The application must also provide a Python or shell-based topic creation step.

# Python Application Requirements

Implement the following modules.

## config.py

Centralize configuration:

- Kafka bootstrap servers
- transaction topic name
- inspection topic name
- Ollama base URL
- Ollama model name
- consumer group id

Read from environment variables with sensible local defaults.

## models.py

Define typed data models.

Use Pydantic if useful.

Models:

- BankingTransaction
- RuleFinding
- InspectionResult
- AgentState

## producer.py

Create a Kafka producer that sends demo banking transaction events.

Requirements:

- produce at least 10 predefined sample transactions
- include normal and suspicious examples
- serialize messages as JSON
- use transaction_id as Kafka message key
- print what was sent

Command:

python -m banking_ai.producer

## consumer.py

Create a Kafka consumer that reads transaction events.

Requirements:

- subscribe to banking.transactions
- deserialize JSON
- pass each transaction to the LangGraph agent
- stream the inspection result to the terminal
- commit offsets only after successful inspection if possible
- keep the implementation simple and readable

Command:

python -m banking_ai.consumer

## rules.py

Implement deterministic inspection rules.

Function:

inspect_transaction_rules(transaction: BankingTransaction) -> list[RuleFinding]

Rules must be easy to read and beginner-friendly.

## ollama_client.py

Implement a minimal local Ollama client.

Requirements:

- use httpx or requests
- call local Ollama API
- support streaming response
- default URL: http://localhost:11434
- no external API keys
- handle the case where Ollama is not running
- handle the case where the model is missing
- provide clear error messages

## graph.py

Build a simple LangGraph workflow.

The graph should have these conceptual nodes:

1. load_transaction
2. apply_rules
3. generate_ai_explanation
4. finalize_result

The state should contain:

- transaction
- rule findings
- suspicious flag
- AI explanation text
- final inspection result

The graph does not need to be complex.
The goal is learning.

The agent should stream the explanation from Ollama where possible.

## cli.py

Optional helper CLI.

Commands may include:

- produce
- consume
- inspect-one

Keep this simple.

# Streaming Requirement

The consumer must show AI output progressively in the terminal.

Example terminal output:

Received transaction: txn-1004

Rule findings:
- amount_greater_than_1000
- foreign_country

AI inspection:
This transaction should be reviewed because ...

Final result:
SUSPICIOUS

# README Requirements

Create a strong README.md.

The README must explain:

1. What this project is
2. What it is not
3. Architecture overview
4. Kafka basics explained simply
5. Local AI basics explained simply
6. LangGraph role
7. How to install dependencies
8. How to start Kafka
9. How to start Ollama
10. How to pull a local Ollama model
11. How to produce demo transactions
12. How to consume and inspect transactions
13. Troubleshooting
14. Learning exercises

Include commands such as:

ollama serve
ollama pull llama3.2
./scripts/start.sh
./scripts/create_topics.sh
python -m banking_ai.producer
python -m banking_ai.consumer

# README Architecture Diagram

Include this simple Mermaid diagram:

```mermaid
flowchart LR
    A[Demo Transaction Producer] --> B[Kafka Topic: banking.transactions]
    B --> C[Kafka Consumer]
    C --> D[Deterministic Rules]
    D --> E[LangGraph Agent]
    E --> F[Ollama Local LLM]
    F --> G[Streamed Terminal Explanation]
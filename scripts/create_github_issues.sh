#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

require_gh_auth() {
  if ! gh auth status >/dev/null 2>&1; then
    echo "GitHub CLI is not authenticated."
    echo "Run: gh auth login"
    exit 1
  fi
}

ensure_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if ! gh label list --limit 200 --json name --jq '.[].name' | grep -Fxq "$name"; then
    gh label create "$name" --color "$color" --description "$description" \
      || echo "Label already exists or could not be created: $name"
  fi
}

issue_exists() {
  local title="$1"
  gh issue list \
    --state all \
    --search "$title in:title" \
    --limit 50 \
    --json title \
    --jq '.[].title' | grep -Fxq "$title"
}

create_issue() {
  local id="$1"
  local title="$2"
  local labels="$3"
  local body_file="$tmp_dir/$id.md"

  cat > "$body_file"

  if issue_exists "$title"; then
    echo "Skipping existing issue: $title"
    return
  fi

  gh issue create \
    --title "$title" \
    --label "$labels" \
    --body-file "$body_file"
}

cd "$repo_root"
require_gh_auth

ensure_label "learning" "0E8A16" "Learning-project scope and teaching value"
ensure_label "kafka" "1D76DB" "Kafka topic, producer, consumer, or offset behavior"
ensure_label "infrastructure" "5319E7" "Local runtime and container setup"
ensure_label "producer" "FBCA04" "Kafka producer behavior"
ensure_label "consumer" "D93F0B" "Kafka consumer behavior"
ensure_label "rules" "BFDADC" "Deterministic inspection rules"
ensure_label "testing" "C5DEF5" "Automated tests and verification"
ensure_label "models" "F9D0C4" "Typed data models"
ensure_label "python" "3572A5" "Python implementation"
ensure_label "langgraph" "7057FF" "LangGraph workflow"
ensure_label "ai" "A2EEEF" "Local AI behavior"
ensure_label "ollama" "000000" "Ollama local inference"
ensure_label "streaming" "006B75" "Progressive terminal output"
ensure_label "developer-experience" "D4C5F9" "Scripts and local workflow"
ensure_label "documentation" "0075CA" "README and learning docs"

create_issue "gh-001" "Add local Kafka broker in KRaft mode" "learning,kafka,infrastructure" <<'EOF'
Create a Docker Compose setup with one local Kafka broker in KRaft mode and no ZooKeeper.

Acceptance criteria:

- `./scripts/start.sh` starts Kafka through Docker Compose.
- `./scripts/stop.sh` stops Kafka.
- Kafka exposes `localhost:9092`.
- The setup is local-only and does not use cloud Kafka.

Traceability: LI-001, LI-008.
EOF

create_issue "gh-002" "Implement demo transaction producer" "learning,kafka,producer" <<'EOF'
Create a Python Kafka producer that sends predefined fake banking transactions to `banking.transactions`.

Acceptance criteria:

- `python -m banking_ai.producer` sends at least 10 transactions.
- Message key is `transaction_id`.
- Message value is a JSON transaction payload.
- The producer prints what it queued and what Kafka acknowledged.

Traceability: LI-002, LI-005.
EOF

create_issue "gh-003" "Implement transaction consumer with manual offset commit" "learning,kafka,consumer" <<'EOF'
Create a Python Kafka consumer that reads transactions, inspects them, and commits offsets only after successful inspection.

Acceptance criteria:

- `python -m banking_ai.consumer --max-messages 10` consumes a bounded demo run.
- The consumer uses the configured consumer group id.
- The consumer starts from earliest messages for a new group.
- Invalid messages are handled clearly.
- Ollama failure does not silently commit the inspected message.

Traceability: LI-003, LI-004, LI-007.
EOF

create_issue "gh-004" "Implement deterministic transaction rules" "learning,rules,testing" <<'EOF'
Implement simple first-pass inspection rules before any LLM explanation is generated.

Acceptance criteria:

- `amount > 1000` is suspicious.
- `country not in ["DE", "NL", "FR", "AT"]` is suspicious.
- `transaction_type == "cash_withdrawal" and amount > 500` is suspicious.
- Merchant names containing `crypto`, `casino`, or `unknown` are suspicious.
- Unit tests cover normal and suspicious examples.

Traceability: LI-004.
EOF

create_issue "gh-005" "Add typed Pydantic models" "learning,models,python" <<'EOF'
Define simple Pydantic v2 models for transactions, rule findings, final inspection results, and LangGraph state.

Acceptance criteria:

- `BankingTransaction` validates the demo JSON event shape.
- `RuleFinding` records rule id, reason, relevant fields, and suspicious flag.
- `InspectionResult` records final status and explanation.
- `AgentState` represents graph workflow state.
- Unit tests cover model validation.

Traceability: LI-005.
EOF

create_issue "gh-006" "Build LangGraph inspection workflow" "learning,langgraph,ai" <<'EOF'
Use a real LangGraph `StateGraph` to organize the inspection as state transitions.

Acceptance criteria:

- The graph has conceptual nodes for `load_transaction`, `apply_rules`, `generate_ai_explanation`, and `finalize_result`.
- The graph combines deterministic findings with the AI explanation.
- A unit test verifies graph behavior without Kafka, Ollama, Docker, or network access.

Traceability: LI-004, LI-006, LI-010.
EOF

create_issue "gh-007" "Add local Ollama streaming client" "learning,ollama,streaming" <<'EOF'
Create a minimal `httpx` client for Ollama `/api/generate` that streams response chunks to the terminal.

Acceptance criteria:

- The client uses `OLLAMA_BASE_URL` and `OLLAMA_MODEL` defaults.
- The client streams chunks progressively.
- Missing Ollama and missing model errors are clear.
- No external AI API, hosted tracing, cloud service, or API key is used.

Traceability: LI-007.
EOF

create_issue "gh-008" "Add beginner-friendly scripts" "learning,developer-experience" <<'EOF'
Add simple bash scripts for the main learning flow.

Acceptance criteria:

- Scripts use `set -euo pipefail`.
- `scripts/start.sh` starts Kafka.
- `scripts/stop.sh` stops Kafka.
- `scripts/create_topics.sh` creates `banking.transactions`.
- `scripts/produce_demo_transactions.sh` runs the producer.
- `scripts/consume_and_inspect.sh` runs the consumer.

Traceability: LI-001, LI-002, LI-003, LI-008.
EOF

create_issue "gh-009" "Write README learning guide" "learning,documentation" <<'EOF'
Document the project for a beginner who wants to understand Kafka basics and local AI streaming.

Acceptance criteria:

- README explains what the project is and is not.
- README explains Kafka, Ollama, LangGraph, rules, offsets, and consumer groups.
- README includes the required Mermaid architecture diagram.
- README includes install, run, test, troubleshooting, and learning exercise commands.
- README links to the traceability matrix.

Traceability: LI-009.
EOF

create_issue "gh-010" "Add infrastructure-free unit tests" "learning,testing" <<'EOF'
Add focused unit tests that verify core behavior without requiring Kafka, Docker, Ollama, or network access.

Acceptance criteria:

- Rule tests cover normal and suspicious transactions.
- Model tests cover validation.
- Graph tests use a fake streaming Ollama client.
- `pytest` passes after installing development dependencies.

Traceability: LI-004, LI-005, LI-006, LI-010.
EOF

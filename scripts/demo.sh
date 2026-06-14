#!/usr/bin/env bash
set -euo pipefail

# Happy-path demo of the full local learning flow. It does not hide any step;
# each numbered step maps to a command you can also run yourself.
#
# Prerequisites:
#   - Rancher Desktop running as the local container runtime (Kubernetes disabled)
#   - Ollama running locally: ollama serve
#   - The configured model pulled:   ollama pull "${OLLAMA_MODEL:-qwen3-coder:30b}"
#   - The project installed:         pip install -e ".[dev]"

PYTHON="${PYTHON:-python3}"

echo "==> [1/5] Start local Kafka + Kafbat UI containers"
./scripts/start.sh

echo "==> Waiting for Kafka to become ready"
sleep 10

echo "==> [2/5] Create Kafka topics"
PYTHON="${PYTHON}" ./scripts/create_topics.sh

echo "==> [3/5] Produce demo transactions"
PYTHON="${PYTHON}" ./scripts/produce_demo_transactions.sh

echo "==> [4/5] Consume and inspect (rules -> LangGraph -> Ollama streaming)"
PYTHON="${PYTHON}" MAX_MESSAGES="${MAX_MESSAGES:-10}" ./scripts/consume_and_inspect.sh

echo "==> [5/5] Demo finished."
echo "Open Kafbat UI:  http://localhost:8080"
echo "Stop containers: ./scripts/stop.sh"

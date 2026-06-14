#!/usr/bin/env bash
set -euo pipefail

# Static verification that does not need Kafka, Ollama, or network access.
# Run this before pushing changes.

PYTHON="${PYTHON:-python3}"

echo "==> Compiling sources (python -m compileall src tests)"
"${PYTHON}" -m compileall -q src tests

echo "==> Running unit tests (python -m pytest)"
"${PYTHON}" -m pytest

echo "==> Validating Docker Compose configuration (docker compose config)"
docker compose config >/dev/null

echo "All checks passed."

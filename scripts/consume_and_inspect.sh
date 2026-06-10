#!/usr/bin/env bash
set -euo pipefail

"${PYTHON:-python3}" -m banking_ai.consumer \
  --max-messages "${MAX_MESSAGES:-10}" \
  --idle-timeout-seconds "${IDLE_TIMEOUT_SECONDS:-30}"

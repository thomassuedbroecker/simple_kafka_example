#!/usr/bin/env bash
set -euo pipefail

python -m banking_ai.consumer --max-messages "${MAX_MESSAGES:-10}"

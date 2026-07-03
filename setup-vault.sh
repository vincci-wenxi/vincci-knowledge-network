#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="${VAULT_ROOT:-$HOME/文希知识库}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Python 3.7+ is required." >&2
    exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/scripts/setup_vault.py" --vault "$VAULT_ROOT"

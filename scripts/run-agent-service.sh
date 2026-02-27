#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
cd "$SCRIPT_DIR/../agent-service" || exit 1
python3 -m pip install -r requirements.txt -q
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

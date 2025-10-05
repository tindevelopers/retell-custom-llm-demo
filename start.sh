#!/bin/bash
# Railway startup script - try multiple Python paths
if [ -f "/opt/venv/bin/python" ]; then
    exec /opt/venv/bin/python -m uvicorn app.server:app --host 0.0.0.0 --port $PORT
elif command -v python3 >/dev/null 2>&1; then
    exec python3 -m uvicorn app.server:app --host 0.0.0.0 --port $PORT
elif command -v python >/dev/null 2>&1; then
    exec python -m uvicorn app.server:app --host 0.0.0.0 --port $PORT
else
    echo "No Python executable found!"
    exit 1
fi

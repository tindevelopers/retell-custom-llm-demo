#!/bin/bash
# Railway startup script
exec /opt/venv/bin/python -m uvicorn app.server:app --host 0.0.0.0 --port $PORT

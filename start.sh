#!/bin/bash
# Railway startup script
exec python3 -m uvicorn app.server:app --host 0.0.0.0 --port $PORT

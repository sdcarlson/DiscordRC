#!/usr/bin/env bash

cd "$(dirname "$0")/../.." || exit 1  # cd to `DiscordRC/`
source api/venv/bin/activate

export DATABASE_NAME="test-db"
uvicorn api.main:app --log-level critical &
UVI_PID=$!
sleep 1

cd api/tests || exit
pytest -v
PYTEST_STATUS=$?
kill $UVI_PID

python3 cleanup.py
exit $PYTEST_STATUS

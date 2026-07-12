#!/usr/bin/env bash
# Wait for Postgres, apply migrations, seed reference data, then start the API.
set -euo pipefail

echo "[entrypoint] waiting for database..."
python - <<'PY'
import os
import time

from sqlalchemy import create_engine, text

url = os.environ["DATABASE_URL"]
for attempt in range(60):
    try:
        create_engine(url).connect().execute(text("SELECT 1"))
        print("[entrypoint] database is ready")
        break
    except Exception as exc:  # noqa: BLE001
        print(f"[entrypoint] db not ready ({attempt}): {exc}")
        time.sleep(2)
else:
    raise SystemExit("[entrypoint] database never became ready")
PY

echo "[entrypoint] running migrations..."
alembic upgrade head

echo "[entrypoint] seeding reference data..."
python -m app.db.seed || echo "[entrypoint] seed skipped/failed (non-fatal)"

echo "[entrypoint] starting API..."
exec "$@"

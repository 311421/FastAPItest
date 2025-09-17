#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH=/app:${PYTHONPATH:-}
cd /app

# Wait for Postgres
if [ -n "${DATABASE_URL}" ]; then
  python - <<'PY'
import sys, os, time
import asyncio
from urllib.parse import urlparse
import asyncpg

url = os.environ.get('DATABASE_URL', '')
if not url:
    sys.exit(0)

parsed = urlparse(url.replace('postgresql+asyncpg', 'postgresql'))
host = parsed.hostname or 'localhost'
port = parsed.port or 5432
user = parsed.username or 'postgres'
password = parsed.password or ''
database = parsed.path.lstrip('/') or 'postgres'

async def wait_db():
    for i in range(60):
        try:
            conn = await asyncpg.connect(host=host, port=port, user=user, password=password, database=database)
            await conn.close()
            print('DB is up')
            return
        except Exception as e:
            print(f'Waiting for DB... {e}')
            await asyncio.sleep(1)
    print('DB not available, exiting')
    sys.exit(1)

asyncio.run(wait_db())
PY
fi

# Run migrations with retries (DB might be up but not ready)
for i in {1..30}; do
  if alembic upgrade head; then
    echo "Alembic migrations applied"
    break
  fi
  echo "Alembic not ready yet, retry $i/30..."
  sleep 2
done

# Start app
exec uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}



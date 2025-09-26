#!/usr/bin/env sh
set -euo pipefail

# Ensure Flask can find your app factory
export FLASK_APP="${FLASK_APP:-ghostbusters_wiki/wsgi.py:create_app}"

# 1) Initialize Alembic if needed
if [ ! -d "/app/migrations" ]; then
  echo "[migrations] not found — initializing Alembic..."
  flask db init
fi

# 2) Create initial migration if none exists
if [ ! -d "/app/migrations/versions" ] || [ -z "$(ls -A /app/migrations/versions 2>/dev/null || true)" ]; then
  echo "No migration versions — autogenerating initial migration..."
  # If there are no model changes, this will print 'Detected no changes' and do nothing (safe).
  flask db migrate -m "init" || true
fi

# 3) Apply migrations (safe to run repeatedly)
echo "Upgrading database..."
flask db upgrade

# 4) Start the app
exec gunicorn -w "${WEB_CONCURRENCY:-2}" -b "0.0.0.0:${PORT:-8000}" wsgi:app

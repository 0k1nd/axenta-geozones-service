#!/bin/sh
set -e

if [ ! -x /opt/venv/bin/python ]; then
  echo "Bootstrapping /opt/venv with uv sync..."
  uv sync --locked
fi

sleep 3

if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."
  until nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
    sleep 1
  done
  echo "Postgres is up."
fi

if [ "$RUN_DJANGO_MIGRATIONS" = "true" ]; then
    uv run python manage.py makemigrations --noinput || true
    uv run python manage.py migrate --noinput
    uv run python manage.py collectstatic --noinput
fi

exec "$@"

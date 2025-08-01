#!/bin/sh

set -e

if [ -n "$PG_HOST" ] && [ -n "$PG_PORT" ]; then
    echo "Checking PostgreSQL connection at $PG_HOST:$PG_PORT"
    while ! nc -z $PG_HOST $PG_PORT; do
        sleep 0.5
        echo "Waiting for PostgreSQL..."
    done
    echo "PostgreSQL is available!"
fi

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Applying database migrations..."
    cd /app/src/bot
    alembic upgrade head
    cd /app
fi

echo "Starting Telegram Bot..."
exec python -m src.bot.app
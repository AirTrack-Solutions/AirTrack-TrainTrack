#!/bin/sh
# wait-for-mariadb.sh
# Waits for MariaDB to be ready before starting the app.

HOST="${DB_HOST:-traintrack-db}"
PORT="${DB_PORT:-3306}"
TIMEOUT="${DB_TIMEOUT:-60}"

echo "Waiting for MariaDB at ${HOST}:${PORT} (timeout ${TIMEOUT}s)…"

elapsed=0
until mysql -h"${HOST}" -P"${PORT}" -u"${DB_USER}" -p"${DB_PASSWORD}" -e "SELECT 1" > /dev/null 2>&1; do
    sleep 2
    elapsed=$((elapsed + 2))
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ MariaDB did not become ready in time. Exiting."
        exit 1
    fi
done

echo "MariaDB is up."
exec "$@"

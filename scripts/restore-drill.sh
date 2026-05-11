#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
SERVICE="${POSTGRES_SERVICE:-pg}"
DB="${POSTGRES_DB:-pgfound}"
USER="${POSTGRES_USER:-pgfound}"
DUMP_PATH="/tmp/pgfound-restore-drill.dump"

docker compose -f "${COMPOSE_FILE}" up -d "${SERVICE}" >/dev/null

docker compose -f "${COMPOSE_FILE}" exec -T "${SERVICE}" psql \
  -U "${USER}" -d "${DB}" -v ON_ERROR_STOP=1 <<'SQL'
CREATE SCHEMA IF NOT EXISTS _admin;
DROP TABLE IF EXISTS _admin.restore_drill_probe;
CREATE TABLE _admin.restore_drill_probe (
    id integer PRIMARY KEY,
    marker text NOT NULL
);
INSERT INTO _admin.restore_drill_probe (id, marker)
VALUES (1, 'restore-drill-ok');
SQL

docker compose -f "${COMPOSE_FILE}" exec -T "${SERVICE}" pg_dump \
  -U "${USER}" -d "${DB}" -Fc -f "${DUMP_PATH}"

docker compose -f "${COMPOSE_FILE}" exec -T "${SERVICE}" psql \
  -U "${USER}" -d postgres -v ON_ERROR_STOP=1 <<SQL
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '${DB}'
  AND pid <> pg_backend_pid();
SELECT pg_terminate_backend(active_pid)
FROM pg_replication_slots
WHERE database = '${DB}'
  AND active_pid IS NOT NULL;
SELECT pg_drop_replication_slot(slot_name)
FROM pg_replication_slots
WHERE database = '${DB}';
DROP DATABASE IF EXISTS ${DB};
CREATE DATABASE ${DB} OWNER ${USER};
SQL

docker compose -f "${COMPOSE_FILE}" exec -T "${SERVICE}" pg_restore \
  -U "${USER}" -d "${DB}" --clean --if-exists "${DUMP_PATH}"

actual="$(
  docker compose -f "${COMPOSE_FILE}" exec -T "${SERVICE}" psql \
    -U "${USER}" -d "${DB}" -Atc \
    "SELECT marker FROM _admin.restore_drill_probe WHERE id = 1;"
)"

if [[ "${actual}" != "restore-drill-ok" ]]; then
  echo "restore drill failed: expected restore-drill-ok, got ${actual}" >&2
  exit 1
fi

echo "restore drill passed: ${actual}"

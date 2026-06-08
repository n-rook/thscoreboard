#!/usr/bin/env bash
set -euo pipefail

: "${LOCAL_DATABASE_PASSWORD:?LOCAL_DATABASE_PASSWORD is required}"

psql -v ON_ERROR_STOP=1 \
  -v thscoreboard_password="$LOCAL_DATABASE_PASSWORD" <<'SQL'
CREATE USER thscoreboard WITH LOGIN PASSWORD :'thscoreboard_password';
SQL

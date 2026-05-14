#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "--dry-run" ]; then
  cat <<'EOF'
uv run ruff check .
uv run ruff format --check .
uv run pgfound content validate --strict
uv run pgfound content lint --strict
uv run pgfound decision catalog check
uv run pgfound decision rules lint
uv run pgfound docs check
uv run pytest -q -m 'not docker'
EOF
  exit 0
fi

uv run ruff check .
uv run ruff format --check .
uv run pgfound content validate --strict
uv run pgfound content lint --strict
uv run pgfound decision catalog check
uv run pgfound decision rules lint
uv run pgfound docs check
uv run pytest -q -m 'not docker'

#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
  exit 0
fi

args=(content validate --strict --schema-only)
for path in "$@"; do
  if [ -f "$path" ]; then
    args+=(--paths "$path")
  fi
done

if [ "${#args[@]}" -eq 4 ]; then
  exit 0
fi

uv run pgfound "${args[@]}"

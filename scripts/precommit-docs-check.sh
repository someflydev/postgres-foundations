#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
  exit 0
fi

uv run pgfound docs check

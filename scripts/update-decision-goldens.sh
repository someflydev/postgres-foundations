#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" != "--confirm" ]]; then
  echo "usage: scripts/update-decision-goldens.sh --confirm" >&2
  echo "regenerates decision-engine/fixtures/reports/*.report.{json,md}" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
intake_dir="${repo_root}/decision-engine/fixtures/intakes"
report_dir="${repo_root}/decision-engine/fixtures/reports"

for intake in "${intake_dir}"/*.json; do
  name="$(basename "${intake}" .json)"
  tmp_dir="$(mktemp -d)"
  uv run pgfound decision run "${intake}" --out-dir "${tmp_dir}" --show-scores >/dev/null
  uv run python - "$tmp_dir/report.json" "$report_dir/${name}.report.json" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
report = json.loads(source.read_text(encoding="utf-8"))
report["generated_at"] = "2026-05-12T00:00:00Z"
target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
  cp "${tmp_dir}/report.md" "${report_dir}/${name}.report.md"
  rm -rf "${tmp_dir}"
done

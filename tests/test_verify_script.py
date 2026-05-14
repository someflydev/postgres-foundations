import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-all.sh"


def test_verify_all_script_exists_and_is_executable() -> None:
    assert SCRIPT.exists()
    assert os.access(SCRIPT, os.X_OK)


def test_verify_all_dry_run_lists_expected_commands() -> None:
    result = subprocess.run(
        [str(SCRIPT), "--dry-run"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.splitlines() == [
        "uv run ruff check .",
        "uv run ruff format --check .",
        "uv run pgfound content validate --strict",
        "uv run pgfound content lint --strict",
        "uv run pgfound decision catalog check",
        "uv run pgfound decision rules lint",
        "uv run pgfound docs check",
        "uv run pytest -q -m 'not docker'",
    ]

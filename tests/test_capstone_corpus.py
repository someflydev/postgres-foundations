import json
import subprocess
from pathlib import Path

import pytest

from pgfound import paths
from pgfound.content import seed as content_seed
from pgfound.content import validate
from pgfound.lab import harness

CAPSTONE_IDS = ("01-multi-tenant-saas-crm", "02-scheduling-availability")


def test_capstone_metadata_and_composed_rubrics_validate() -> None:
    report = validate.validate_content(
        path_globs=(
            "capstones/**/*.json",
            "rubrics/default/*.rubric.json",
        )
    )

    assert report.ok, [issue.message for issue in report.errors]
    assert report.by_kind["capstone"] == 2
    assert report.by_kind["rubric"] >= 8


def test_capstone_layout_contains_required_files() -> None:
    required = {
        "capstone.json",
        "narrative.md",
        "brief.md",
        "constraints.md",
        "acceptance-criteria.md",
        "starter/schema-skeleton.sql",
        "starter/seed-sample.csv",
        "starter/README.md",
        "reference/schema.sql",
        "reference/indexes.sql",
        "reference/rls-policies.sql",
        "reference/critical-queries.sql",
        "reference/operational-runbook.md",
        "reference/writeup.md",
        "rubric.json",
    }
    for capstone_id in CAPSTONE_IDS:
        capstone_dir = paths.CAPSTONES_DIR / capstone_id
        missing = [name for name in sorted(required) if not (capstone_dir / name).is_file()]
        assert missing == []


def test_capstone_markdown_word_counts_match_prompt_contract() -> None:
    for capstone_id in CAPSTONE_IDS:
        capstone_dir = paths.CAPSTONES_DIR / capstone_id
        narrative_words = _word_count(capstone_dir / "narrative.md")
        brief_words = _word_count(capstone_dir / "brief.md")
        writeup_words = _word_count(capstone_dir / "reference" / "writeup.md")
        assert 800 <= narrative_words <= 1200
        assert brief_words >= 550
        assert 2500 <= writeup_words <= 3500


def test_capstone_rubric_composition_weights_sum_to_one() -> None:
    for rubric_path in sorted(paths.CAPSTONES_DIR.glob("*/rubric.json")):
        data = json.loads(rubric_path.read_text(encoding="utf-8"))
        total = sum(entry["weight"] for entry in data.get("extends", []))
        total += sum(dimension["weight"] for dimension in data.get("own_dimensions", []))
        assert total == 1.0


def test_reference_schema_sql_has_no_psql_include_meta_commands() -> None:
    for capstone_id in CAPSTONE_IDS:
        schema = (paths.CAPSTONES_DIR / capstone_id / "reference" / "schema.sql").read_text(
            encoding="utf-8"
        )
        assert "\\ir" not in schema


def test_scheduling_concurrency_scenario_parses() -> None:
    scenario_path = paths.REPO_ROOT / "scenarios/concurrency/scheduling-double-booking.yaml"
    scenario = harness.load_scenario(scenario_path)

    assert scenario["name"] == "scheduling-double-booking"


def test_reference_schema_applies_when_psql_is_available(tmp_path: Path) -> None:
    if subprocess.run(["which", "psql"], capture_output=True).returncode != 0:
        pytest.skip("psql is not available")
    if not _database_available():
        pytest.skip("lab database is not available")

    for capstone_id in CAPSTONE_IDS:
        schema_name = f"capstone_test_{capstone_id.replace('-', '_')}"
        reference_dir = paths.CAPSTONES_DIR / capstone_id / "reference"
        command = [
            "psql",
            content_seed.database_url(),
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;",
            "-c",
            f"CREATE SCHEMA {schema_name};",
            "-c",
            f"SET search_path TO {schema_name}, public;",
            "-f",
            str(reference_dir / "schema.sql"),
            "-f",
            str(reference_dir / "indexes.sql"),
            "-f",
            str(reference_dir / "rls-policies.sql"),
            "-f",
            str(reference_dir / "critical-queries.sql"),
            "-c",
            f"DROP SCHEMA {schema_name} CASCADE;",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


def _word_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def _database_available() -> bool:
    result = subprocess.run(
        ["psql", content_seed.database_url(), "-c", "SELECT 1"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0

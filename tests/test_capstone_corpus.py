import json
import subprocess
from pathlib import Path

import pytest

from pgfound import paths
from pgfound.content import seed as content_seed
from pgfound.content import validate
from pgfound.lab import harness

CAPSTONE_IDS = (
    "01-multi-tenant-saas-crm",
    "02-scheduling-availability",
    "03-event-heavy-ops",
    "04-modernization-bridge",
    "05-geo-logistics-platform",
    "06-ai-knowledge-platform",
    "07-observability-event-analytics",
    "08-modernization-bridge-extensions",
)

CORE_CAPSTONE_IDS = CAPSTONE_IDS[:4]


def test_capstone_metadata_and_composed_rubrics_validate() -> None:
    report = validate.validate_content(
        path_globs=(
            "capstones/**/*.json",
            "rubrics/default/*.rubric.json",
        )
    )

    assert report.ok, [issue.message for issue in report.errors]
    assert report.by_kind["capstone"] == 8
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


def test_original_capstone_markdown_word_counts_match_prompt_contract() -> None:
    for capstone_id in ("01-multi-tenant-saas-crm", "02-scheduling-availability"):
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


def test_new_capstones_include_prompt_specific_artifacts() -> None:
    event_dir = paths.CAPSTONES_DIR / "03-event-heavy-ops"
    bridge_dir = paths.CAPSTONES_DIR / "04-modernization-bridge"

    assert (event_dir / "reference" / "retention.sql").is_file()
    assert "TimescaleDB" in (event_dir / "reference" / "writeup.md").read_text(encoding="utf-8")
    assert "top-N" in (event_dir / "brief.md").read_text(encoding="utf-8") or "Top-N" in (
        event_dir / "capstone.json"
    ).read_text(encoding="utf-8")

    assert (bridge_dir / "reference" / "fdw-wiring.sql").is_file()
    bridge_queries = (bridge_dir / "reference" / "critical-queries.sql").read_text(encoding="utf-8")
    assert bridge_queries.count(";") >= 8
    bridge_writeup = (bridge_dir / "reference" / "writeup.md").read_text(encoding="utf-8")
    assert "Promote to logical replication when X" in bridge_writeup
    assert "Citus" in bridge_writeup


def test_scheduling_concurrency_scenario_parses() -> None:
    scenario_path = paths.REPO_ROOT / "scenarios/concurrency/scheduling-double-booking.yaml"
    scenario = harness.load_scenario(scenario_path)

    assert scenario["name"] == "scheduling-double-booking"


def test_reference_schema_applies_when_psql_is_available(tmp_path: Path) -> None:
    if subprocess.run(["which", "psql"], capture_output=True).returncode != 0:
        pytest.skip("psql is not available")
    if not _database_available():
        pytest.skip("lab database is not available")

    for capstone_id in CORE_CAPSTONE_IDS:
        schema_name = f"capstone_test_{capstone_id.replace('-', '_')}"
        reference_dir = paths.CAPSTONES_DIR / capstone_id / "reference"
        command = [
            "psql",
            content_seed.database_url(),
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            "BEGIN;",
            "-c",
            "DROP SERVER IF EXISTS legacy_monolith CASCADE;",
            "-c",
            "DROP SCHEMA IF EXISTS legacy_fdw CASCADE;",
            "-c",
            "DROP SCHEMA IF EXISTS new_service CASCADE;",
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
            "-c",
            "ROLLBACK;",
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

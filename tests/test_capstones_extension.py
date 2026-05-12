import json

from pgfound import paths
from pgfound.content import validate

EXTENSION_CAPSTONE_IDS = (
    "05-geo-logistics-platform",
    "06-ai-knowledge-platform",
    "07-observability-event-analytics",
    "08-modernization-bridge-extensions",
)


def test_extension_capstones_validate_and_have_balanced_rubrics() -> None:
    report = validate.validate_content(
        path_globs=(
            "capstones/**/*.json",
            "rubrics/default/*.rubric.json",
        )
    )

    assert report.ok, [issue.message for issue in report.errors]

    for capstone_id in EXTENSION_CAPSTONE_IDS:
        capstone_dir = paths.CAPSTONES_DIR / capstone_id
        assert (capstone_dir / "capstone.json").is_file()
        rubric = json.loads((capstone_dir / "rubric.json").read_text(encoding="utf-8"))
        total = sum(entry["weight"] for entry in rubric.get("extends", []))
        total += sum(dimension["weight"] for dimension in rubric.get("own_dimensions", []))
        assert total == 1.0
        extension_weight = sum(
            entry["weight"]
            for entry in rubric.get("extends", [])
            if entry["rubric_id"] == "extension-posture"
        )
        assert extension_weight >= 0.20


def test_extension_capstones_include_prompt_specific_artifacts() -> None:
    geo = paths.CAPSTONES_DIR / "05-geo-logistics-platform"
    ai = paths.CAPSTONES_DIR / "06-ai-knowledge-platform"
    observability = paths.CAPSTONES_DIR / "07-observability-event-analytics"
    bridge = paths.CAPSTONES_DIR / "08-modernization-bridge-extensions"

    assert "postgis" in (geo / "reference" / "schema.sql").read_text(encoding="utf-8").lower()
    assert "pg_partman" in (geo / "reference" / "schema.sql").read_text(encoding="utf-8")
    assert (
        "pgvector is avoid for now"
        in (geo / "reference" / "writeup.md").read_text(encoding="utf-8").lower()
    )

    ai_schema = (ai / "reference" / "schema.sql").read_text(encoding="utf-8").lower()
    ai_indexes = (ai / "reference" / "indexes.sql").read_text(encoding="utf-8").lower()
    assert "pg_trgm" in ai_schema
    assert "vector" in ai_schema
    assert "hnsw" in ai_indexes
    assert (
        "reciprocal rank fusion"
        in (ai / "reference" / "writeup.md").read_text(encoding="utf-8").lower()
    )

    observability_writeup = (observability / "reference" / "writeup.md").read_text(encoding="utf-8")
    assert "TimescaleDB is later" in observability_writeup
    assert (
        "brin" in (observability / "reference" / "indexes.sql").read_text(encoding="utf-8").lower()
    )

    assert (bridge / "reference" / "fdw-wiring.sql").is_file()
    bridge_writeup = (bridge / "reference" / "writeup.md").read_text(encoding="utf-8")
    assert "Citus is avoid for now" in bridge_writeup
    assert "distribution key" in bridge_writeup


def test_extension_capstone_reference_writeups_match_prompt_contract() -> None:
    for capstone_id in EXTENSION_CAPSTONE_IDS:
        writeup = paths.CAPSTONES_DIR / capstone_id / "reference" / "writeup.md"
        word_count = len(writeup.read_text(encoding="utf-8").split())
        assert 2500 <= word_count <= 3500, writeup

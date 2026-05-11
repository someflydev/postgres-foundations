import json

from pgfound import paths

CAPSTONE_IDS = {
    "01-multi-tenant-saas-crm",
    "02-scheduling-availability",
    "03-event-heavy-ops",
    "04-modernization-bridge",
}


def test_all_four_capstones_are_listed_and_have_balanced_rubrics() -> None:
    actual_ids = {path.parent.name for path in paths.CAPSTONES_DIR.glob("*/capstone.json")}
    assert actual_ids == CAPSTONE_IDS

    for rubric_path in sorted(paths.CAPSTONES_DIR.glob("*/rubric.json")):
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        total = sum(entry["weight"] for entry in rubric.get("extends", []))
        total += sum(dimension["weight"] for dimension in rubric.get("own_dimensions", []))
        assert total == 1.0, rubric_path


def test_reference_schema_exists_for_all_capstones() -> None:
    for capstone_id in CAPSTONE_IDS:
        schema_path = paths.CAPSTONES_DIR / capstone_id / "reference" / "schema.sql"
        assert schema_path.is_file()
        assert "CREATE TABLE" in schema_path.read_text(encoding="utf-8")

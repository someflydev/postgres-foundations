import json

from jsonschema import Draft202012Validator
from test_catalog_forward_refs import PROMPT_41_EXTENSIONS

from pgfound import paths
from pgfound.decision import engine as decision_engine


def test_extensions_catalog_validates_and_has_required_entries() -> None:
    catalog_path = paths.DECISION_ENGINE_DIR / "catalogs" / "extensions.json"
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / "extension.schema.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    assert {entry["id"] for entry in catalog} == PROMPT_41_EXTENSIONS
    pgbouncer = next(entry for entry in catalog if entry["id"] == "pgbouncer")
    assert pgbouncer["kind"] == "operational_tool"
    for entry in catalog:
        assert sorted(validator.iter_errors(entry), key=lambda error: list(error.path)) == []
        assert decision_engine._sentence_count(entry["summary"]) >= 2
        prose_fields = [
            "summary",
            "why_it_exists",
            "when_core_is_enough",
            "workload_fit",
            "operational_cost",
            "replication_backup_implications",
        ]
        word_count = sum(len(entry[field].split()) for field in prose_fields)
        assert 250 <= word_count <= 400, entry["id"]
        assert entry["when_core_is_enough"]
        assert entry["workload_fit"]
        assert entry["operational_cost"]
        assert entry["adoption_triggers"]
        assert entry["not_yet_triggers"]
        assert entry["anti_patterns"]

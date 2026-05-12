import json

from jsonschema import Draft202012Validator
from test_catalog_forward_refs import PROMPT_41_CORE_FEATURES

from pgfound import paths
from pgfound.decision import engine as decision_engine


def test_core_features_catalog_validates_and_has_required_entries() -> None:
    catalog_path = paths.DECISION_ENGINE_DIR / "catalogs" / "postgres_core_features.json"
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / "core-feature.schema.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    assert {entry["id"] for entry in catalog} == PROMPT_41_CORE_FEATURES
    for entry in catalog:
        assert sorted(validator.iter_errors(entry), key=lambda error: list(error.path)) == []
        assert all(entry[field] is not None for field in entry)
        assert decision_engine._sentence_count(entry["summary"]) >= 2
        word_count = len(entry["summary"].split())
        assert 120 <= word_count <= 200, entry["id"]

import json

from jsonschema import Draft202012Validator
from test_catalog_forward_refs import PROMPT_41_TOPOLOGY_PATTERNS

from pgfound import paths
from pgfound.decision import engine as decision_engine


def test_topology_patterns_catalog_validates_and_has_required_entries() -> None:
    catalog_path = paths.DECISION_ENGINE_DIR / "catalogs" / "topology_patterns.json"
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / "topology-pattern.schema.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    assert {entry["id"] for entry in catalog} == PROMPT_41_TOPOLOGY_PATTERNS
    for entry in catalog:
        assert sorted(validator.iter_errors(entry), key=lambda error: list(error.path)) == []
        assert decision_engine._sentence_count(entry["summary"]) >= 2
        assert entry["failure_modes"]

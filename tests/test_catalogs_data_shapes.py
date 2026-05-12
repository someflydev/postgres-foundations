import json

from jsonschema import Draft202012Validator

from pgfound import paths
from pgfound.decision import engine as decision_engine


def test_data_shapes_catalog_validates_and_has_required_entries() -> None:
    catalog_path = paths.DECISION_ENGINE_DIR / "catalogs" / "data_shapes.json"
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / "data-shape.schema.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    ids = {entry["id"] for entry in catalog}
    assert ids == {
        "relational_core",
        "semi_structured_jsonb",
        "arrays_small_sets",
        "ranges_windows",
        "multiranges_availability",
        "hierarchy_paths",
        "full_text_docs",
        "geospatial",
        "append_only_events",
        "time_series_metrics",
        "embeddings_vectors",
        "foreign_postgres_access",
    }
    for entry in catalog:
        assert sorted(validator.iter_errors(entry), key=lambda error: list(error.path)) == []
        assert all(entry[field] is not None for field in entry)
        assert decision_engine._sentence_count(entry["summary"]) >= 2


def test_data_shape_references_resolve_after_prompt_41_catalogs_land() -> None:
    result = decision_engine.check_catalogs()

    assert result["errors"] == []
    assert result["warnings"] == []

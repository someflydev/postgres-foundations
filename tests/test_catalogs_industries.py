import json

from jsonschema import Draft202012Validator

from pgfound import paths
from pgfound.decision import engine as decision_engine


def _load(name: str):
    path = paths.DECISION_ENGINE_DIR / "catalogs" / name
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_entries(catalog_name: str, schema_name: str):
    catalog = _load(catalog_name)
    schema = json.loads(
        (paths.DECISION_ENGINE_DIR / "schemas" / schema_name).read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    for entry in catalog:
        errors = sorted(validator.iter_errors(entry), key=lambda error: list(error.path))
        assert errors == []
    return catalog


def test_industries_catalog_validates_and_has_required_entries() -> None:
    catalog = _validate_entries("industries.json", "industry.schema.json")

    ids = {entry["id"] for entry in catalog}
    assert ids == {
        "saas_multi_tenant",
        "fintech_payments",
        "healthcare_ops",
        "ecommerce_marketplace",
        "logistics_geo",
        "observability_iot",
        "knowledge_ai",
        "modernization_bridge",
    }
    for entry in catalog:
        assert all(entry[field] for field in entry)
        assert decision_engine._sentence_count(entry["summary"]) >= 2


def test_industry_cross_references_resolve() -> None:
    result = decision_engine.check_catalogs()

    assert result["errors"] == []

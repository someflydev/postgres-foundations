import json

from click.testing import CliRunner
from jsonschema import Draft202012Validator

from pgfound import paths
from pgfound.cli import main
from pgfound.decision import engine as decision_engine


def test_workload_patterns_catalog_validates_and_has_required_entries() -> None:
    catalog_path = paths.DECISION_ENGINE_DIR / "catalogs" / "workload_patterns.json"
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / "workload-pattern.schema.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    ids = {entry["id"] for entry in catalog}
    assert ids == {
        "oltp_heavy",
        "search_heavy",
        "read_heavy",
        "append_heavy",
        "analytics_adjacent",
        "replication_fanout",
        "migration_bridge",
        "geo_query_heavy",
        "semantic_retrieval",
        "strong_tenant_locality",
    }
    for entry in catalog:
        assert sorted(validator.iter_errors(entry), key=lambda error: list(error.path)) == []
        assert all(entry[field] is not None for field in entry)
        assert decision_engine._sentence_count(entry["summary"]) >= 2


def test_decision_catalog_cli_lists_and_checks() -> None:
    runner = CliRunner()

    list_result = runner.invoke(main, ["decision", "catalog", "list", "--kind", "industry"])
    assert list_result.exit_code == 0, list_result.output
    assert "saas_multi_tenant" in list_result.output
    assert "fintech_payments" in list_result.output

    check_result = runner.invoke(main, ["decision", "catalog", "check"])
    assert check_result.exit_code == 0, check_result.output
    assert "error" not in check_result.output.lower()

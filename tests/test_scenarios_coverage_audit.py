from click.testing import CliRunner

from pgfound.cli import main
from pgfound.decision import engine, scenarios


def test_scenario_coverage_audit_has_row_for_every_extension() -> None:
    catalog_slugs = {entry["id"] for entry in engine.load_catalog("extension")}
    rows = scenarios.extension_coverage()

    assert {row.extension_slug for row in rows} == catalog_slugs
    assert all(
        row.recommend_now + row.candidate_later + row.not_enough_evidence + row.avoid_for_now > 0
        for row in rows
    )


def test_decision_scenarios_audit_cli_renders_extension_table() -> None:
    result = CliRunner().invoke(main, ["decision", "scenarios", "audit"])

    assert result.exit_code == 0
    assert "decision scenario extension coverage" in result.output
    assert "pg_stat_statements" in result.output
    assert "pgvector" in result.output

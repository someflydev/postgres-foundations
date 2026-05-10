from click.testing import CliRunner

from pgfound import paths
from pgfound.cli import main
from pgfound.lab import explain


def test_explain_load_plan_accepts_fixture_paths() -> None:
    plan = explain.load_plan(str(paths.REPO_ROOT / "tests/fixtures/plans/seq_scan.json"))

    summary = explain.summarize_plan(plan)

    assert summary.node_types == ("Seq Scan",)
    assert summary.actual_rows == 4500


def test_lab_explain_diffs_fixture_plans_without_database() -> None:
    before = paths.REPO_ROOT / "tests/fixtures/plans/seq_scan.json"
    after = paths.REPO_ROOT / "tests/fixtures/plans/index_scan.json"

    result = CliRunner().invoke(
        main,
        ["lab", "explain", "--baseline", str(before), "--compare", str(after)],
    )

    assert result.exit_code == 0, result.output
    assert "Plan comparison" in result.output
    assert "Seq Scan" in result.output
    assert "Index Scan" in result.output
    assert "execution time ms" in result.output

import json

from click.testing import CliRunner

from pgfound import paths
from pgfound.cli import main
from pgfound.decision.engine import validate_report


def test_decision_run_writes_populated_valid_report(tmp_path) -> None:
    intake = paths.DECISION_ENGINE_DIR / "fixtures" / "intakes" / "saas-multi-tenant-minimal.json"
    result = CliRunner().invoke(
        main,
        ["decision", "run", str(intake), "--out-dir", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    assert "report.json" in result.output
    assert (tmp_path / "report.md").is_file()

    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    validate_report(report)
    assert report["intake_id"] == "saas-multi-tenant-minimal"
    assert report["recommendations"]
    assert any(item["target_slug"] == "row_level_security" for item in report["recommendations"])

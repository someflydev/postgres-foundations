import json

from pgfound import __version__, paths
from pgfound.decision import engine


def _masked(report: dict) -> dict:
    masked = dict(report)
    masked["generated_at"] = "<generated_at>"
    masked["engine_version"] = __version__
    return masked


def test_fixture_json_reports_match_goldens_with_masked_dynamic_fields() -> None:
    intake_dir = paths.DECISION_ENGINE_DIR / "fixtures" / "intakes"
    report_dir = paths.DECISION_ENGINE_DIR / "fixtures" / "reports"

    for intake in sorted(intake_dir.glob("*.json")):
        report = engine.run_decision(intake)
        golden = json.loads(
            (report_dir / f"{report['intake_id']}.report.json").read_text(encoding="utf-8")
        )

        assert _masked(report) == _masked(golden)

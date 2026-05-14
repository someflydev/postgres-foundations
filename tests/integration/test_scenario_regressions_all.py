from __future__ import annotations

import json

from helpers import industry_scenario_dirs

from pgfound.decision import engine


def _masked(report: dict) -> dict:
    masked = dict(report)
    masked["generated_at"] = "<generated_at>"
    return masked


def test_all_industry_scenarios_match_expected_reports() -> None:
    scenario_dirs = industry_scenario_dirs()
    assert len(scenario_dirs) == 24
    for scenario_dir in scenario_dirs:
        report = engine.run_decision(scenario_dir / "intake.json")
        expected = json.loads((scenario_dir / "expected-report.json").read_text(encoding="utf-8"))
        assert _masked(report) == _masked(expected), scenario_dir

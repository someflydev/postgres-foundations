from __future__ import annotations

import json

from helpers import industry_scenario_dirs

from pgfound import paths
from pgfound.decision import engine


def _masked(report: dict) -> dict:
    masked = dict(report)
    masked["generated_at"] = "<generated_at>"
    return masked


def test_industry_scenario_reports_match_goldens_and_expected_outputs() -> None:
    scenario_dirs = industry_scenario_dirs()
    assert len(scenario_dirs) == 24

    for scenario_dir in scenario_dirs:
        scenario = json.loads((scenario_dir / "scenario.json").read_text(encoding="utf-8"))
        actual = engine.run_decision(scenario_dir / "intake.json")
        expected = json.loads((scenario_dir / "expected-report.json").read_text(encoding="utf-8"))
        assert _masked(actual) == _masked(expected), scenario_dir

        by_class: dict[str, set[str]] = {
            "recommend_now": set(),
            "candidate_later": set(),
            "avoid_for_now": set(),
        }
        for recommendation in actual["recommendations"]:
            recommendation_class = recommendation["recommendation_class"]
            if recommendation_class in by_class:
                by_class[recommendation_class].add(recommendation["target_slug"])
        for recommendation_class, expected_slugs in scenario["expected_decision_outputs"].items():
            assert set(expected_slugs) <= by_class[recommendation_class], scenario_dir


def test_all_rules_have_scenario_coverage_or_emit_triage_gap_file() -> None:
    rule_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in paths.DECISION_ENGINE_DIR.glob("rules/**/*.json")
    }
    triggered = set()
    for scenario_dir in industry_scenario_dirs():
        report = engine.run_decision(scenario_dir / "intake.json")
        for recommendation in report["recommendations"]:
            triggered.update(source["rule_id"] for source in recommendation.get("sources", []))

    gaps = sorted(rule_ids - triggered)
    out_dir = paths.TMP_DIR / "integration"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "coverage-gaps.json").write_text(
        json.dumps({"uncovered_rule_slugs": gaps}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    assert rule_ids

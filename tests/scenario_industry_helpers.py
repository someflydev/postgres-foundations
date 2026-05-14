import json
from pathlib import Path

from pgfound import paths
from pgfound.content import validate as content_validate
from pgfound.decision import engine


def industry_scenario_dirs(industry_dir: str) -> list[Path]:
    root = paths.SCENARIOS_DIR / "industries" / industry_dir
    return sorted(path for path in root.iterdir() if path.is_dir())


def assert_industry_scenarios_valid(industry_dir: str, expected_count: int = 3) -> None:
    scenario_dirs = industry_scenario_dirs(industry_dir)
    assert len(scenario_dirs) == expected_count
    for scenario_dir in scenario_dirs:
        assert_scenario_valid(scenario_dir)


def assert_scenario_valid(scenario_dir: Path) -> None:
    report = content_validate.validate_content(
        path_globs=(str(scenario_dir / "scenario.json"),),
    )
    assert report.ok, [issue.message for issue in report.errors]

    scenario = json.loads((scenario_dir / "scenario.json").read_text(encoding="utf-8"))
    actual = engine.run_decision(scenario_dir / "intake.json")
    golden = json.loads((scenario_dir / "expected-report.json").read_text(encoding="utf-8"))
    assert _masked(actual) == _masked(golden)

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
        assert set(expected_slugs) <= by_class[recommendation_class]


def load_report(industry_dir: str, scenario_dir: str) -> dict:
    report_path = (
        paths.SCENARIOS_DIR / "industries" / industry_dir / scenario_dir / "expected-report.json"
    )
    return json.loads(report_path.read_text(encoding="utf-8"))


def slugs_by_class(report: dict, recommendation_class: str) -> set[str]:
    return {
        recommendation["target_slug"]
        for recommendation in report["recommendations"]
        if recommendation["recommendation_class"] == recommendation_class
    }


def slugs_by_class_and_kind(
    report: dict,
    recommendation_class: str,
    kind: str,
) -> set[str]:
    return {
        recommendation["target_slug"]
        for recommendation in report["recommendations"]
        if recommendation["recommendation_class"] == recommendation_class
        and recommendation["kind"] == kind
    }


def _masked(report: dict) -> dict:
    masked = dict(report)
    masked["generated_at"] = "<generated_at>"
    masked["engine_version"] = engine.ENGINE_VERSION
    return masked

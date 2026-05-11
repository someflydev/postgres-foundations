import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, RefResolver

from pgfound import paths
from pgfound.content import validate


def _load_yaml(path: Path) -> dict:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_interview_scenarios_validate_against_dedicated_schema() -> None:
    schema = json.loads(
        (paths.REPO_ROOT / "content-schemas" / "interview-scenario.schema.json").read_text(
            encoding="utf-8"
        )
    )
    resolver = RefResolver(
        base_uri=f"{validate.schema_dir().resolve().as_uri()}/",
        referrer=schema,
        store=validate.schema_store(),
    )
    validator = Draft202012Validator(schema, resolver=resolver)

    scenario_paths = sorted((paths.SCENARIOS_DIR / "interviews").glob("*.yaml"))

    assert len(scenario_paths) == 6
    for scenario_path in scenario_paths:
        errors = sorted(
            validator.iter_errors(_load_yaml(scenario_path)), key=lambda item: item.path
        )
        assert errors == []


def test_interview_scenario_cross_references_are_valid() -> None:
    report = validate.validate_content(
        path_globs=("scenarios/interviews/*.yaml", "rubrics/interview/*.rubric.json")
    )

    assert report.ok, [issue.message for issue in report.errors]


def test_interview_scenario_budgets_do_not_exceed_duration() -> None:
    allowed_layers = set(
        json.loads((paths.REPO_ROOT / "content-schemas" / "common.json").read_text())["$defs"][
            "capability_layer"
        ]["enum"]
    )
    exercise_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in paths.EXERCISES_DIR.rglob("exercise.json")
    }

    for scenario_path in sorted((paths.SCENARIOS_DIR / "interviews").glob("*.yaml")):
        data = _load_yaml(scenario_path)
        assert set(data["capability_layers_required"]) <= allowed_layers
        budget = sum(stage["budget_minutes"] for stage in data["stages"])
        assert budget <= data["duration_minutes"]
        for stage in data["stages"]:
            if "exercise_id" in stage:
                assert stage["exercise_id"] in exercise_ids

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from pgfound.content import validate

SCHEMA_DIR = validate.schema_dir()
KINDS = ("lesson", "exercise", "rubric", "scenario", "capstone")


def _example(kind: str) -> dict:
    path = SCHEMA_DIR / "examples" / f"{kind}.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_each_schema_loads_and_is_draft_2020_12_valid() -> None:
    for schema_path in sorted(SCHEMA_DIR.glob("*.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize("kind", KINDS)
def test_each_example_validates_against_its_schema(kind: str) -> None:
    validator = validate.validator_for(kind)

    errors = sorted(validator.iter_errors(_example(kind)), key=lambda item: item.path)

    assert errors == []


@pytest.mark.parametrize(
    ("kind", "required_field"),
    [
        ("lesson", "id"),
        ("exercise", "lesson_id"),
        ("rubric", "dimensions"),
        ("scenario", "context"),
        ("capstone", "deliverables"),
    ],
)
def test_required_field_violations_have_clear_messages(kind: str, required_field: str) -> None:
    invalid = _example(kind)
    invalid.pop(required_field)
    validator = validate.validator_for(kind)

    messages = [error.message for error in validator.iter_errors(invalid)]

    if kind == "rubric" and required_field == "dimensions":
        assert any("is not valid under any of the given schemas" in message for message in messages)
    else:
        assert f"{required_field!r} is a required property" in messages


def test_rubric_weight_sum_is_enforced_by_content_validator(tmp_path: Path) -> None:
    rubric = _example("rubric")
    rubric["dimensions"][0]["weight"] = 0.5
    path = tmp_path / "rubrics" / "bad-rubric.json"
    path.parent.mkdir()
    path.write_text(json.dumps(rubric), encoding="utf-8")

    report = validate.validate_content(path_globs=(str(path),))

    assert not report.ok
    assert "weights must sum to 1.0" in report.errors[0].message


def test_composed_rubric_weight_sum_includes_extends_and_own_dimensions(tmp_path: Path) -> None:
    rubric = _example("rubric")
    rubric["id"] = "composed-capstone"
    rubric["applies_to"] = "capstone"
    rubric.pop("dimensions")
    rubric["extends"] = [{"rubric_id": "schema-design", "weight": 0.6}]
    rubric["own_dimensions"] = [
        {
            "name": "defense",
            "weight": 0.3,
            "levels": {"0": "none", "1": "weak", "2": "partial", "3": "clear", "4": "strong"},
        }
    ]
    path = tmp_path / "rubrics" / "composed.rubric.json"
    path.parent.mkdir()
    path.write_text(json.dumps(rubric), encoding="utf-8")

    report = validate.validate_content(
        path_globs=(str(path), "rubrics/default/schema-design.rubric.json")
    )

    assert not report.ok
    assert "weights must sum to 1.0" in report.errors[0].message


def test_exercise_dataset_is_required() -> None:
    invalid = _example("exercise")
    invalid.pop("dataset")

    messages = [error.message for error in validate.validator_for("exercise").iter_errors(invalid)]

    assert "'dataset' is a required property" in messages


def test_exercise_hints_are_limited_to_lower_scaffolding_levels() -> None:
    invalid = _example("exercise")
    invalid["scaffolding_level"] = "C"
    invalid["oral_defense_prompts"] = ["Explain why this query is correct."]

    messages = [error.message for error in validate.validator_for("exercise").iter_errors(invalid)]

    assert any("should not be valid under" in message for message in messages)

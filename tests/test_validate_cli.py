import json
from pathlib import Path

from click.testing import CliRunner

from pgfound.cli import main
from pgfound.content import validate


def _example(kind: str) -> dict:
    path = validate.schema_dir() / "examples" / f"{kind}.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_content_validate_passes_for_current_tree_without_examples() -> None:
    result = CliRunner().invoke(main, ["content", "validate"])

    assert result.exit_code == 0
    assert "PASS: checked" in result.output


def test_content_validate_include_examples_passes() -> None:
    result = CliRunner().invoke(main, ["content", "validate", "--include-examples"])

    assert result.exit_code == 0
    assert "PASS: checked 5 file(s)" in result.output


def test_content_validate_reports_valid_and_invalid_temp_content(tmp_path: Path) -> None:
    _write_json(tmp_path / "lessons" / "lesson.json", _example("lesson"))
    _write_json(tmp_path / "rubrics" / "rubric.json", _example("rubric"))
    _write_json(tmp_path / "exercises" / "valid.json", _example("exercise"))

    invalid_exercise = _example("exercise")
    invalid_exercise["id"] = "broken-exercise"
    invalid_exercise["lesson_id"] = "missing-lesson"
    _write_json(tmp_path / "exercises" / "invalid.json", invalid_exercise)

    result = CliRunner().invoke(main, ["content", "validate", "--paths", f"{tmp_path}/**/*.json"])

    assert result.exit_code != 0
    assert "FAIL: checked 4 file(s)" in result.output
    assert "lesson_id 'missing-lesson' does not exist" in result.output


def test_content_validate_strict_turns_warnings_into_errors(tmp_path: Path) -> None:
    _write_json(tmp_path / "scenarios" / "scenario.json", _example("scenario"))

    result = CliRunner().invoke(
        main,
        ["content", "validate", "--strict", "--paths", f"{tmp_path}/**/*.json"],
    )

    assert result.exit_code != 0
    assert "decision-engine catalog missing" in result.output

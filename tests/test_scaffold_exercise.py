import json
from pathlib import Path

from click.testing import CliRunner

from pgfound import paths
from pgfound.cli import main
from pgfound.content import validate


def _write_curriculum_map(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "phases": [
                    {"number": 0, "slug": "reality-before-syntax", "concepts_introduced": []},
                    {
                        "number": 1,
                        "slug": "sql-literacy-basics",
                        "concepts_introduced": ["select"],
                    },
                    {
                        "number": 2,
                        "slug": "relational-joins-and-aggregation",
                        "concepts_introduced": ["join", "aggregate"],
                    },
                    {
                        "number": 5,
                        "slug": "expressive-querying",
                        "concepts_introduced": ["window_function"],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_lesson(lessons_dir: Path) -> Path:
    lesson_dir = lessons_dir / "phase-01-sql-literacy-basics" / "reading-rows" / "fixture-select"
    lesson_dir.mkdir(parents=True, exist_ok=True)
    (lesson_dir / "lesson.json").write_text(
        json.dumps(
            {
                "id": "fixture-select",
                "title": "Fixture SELECT",
                "phase": 1,
                "capability_layer": "schema_literacy",
                "summary": "Fixture lesson.",
                "learning_objectives": ["Read rows.", "Explain a SELECT."],
                "concepts_introduced": ["select"],
                "concepts_not_yet_allowed": ["join"],
                "body_path": "body.md",
                "estimated_time_minutes": 20,
                "status": "draft",
            }
        ),
        encoding="utf-8",
    )
    (lesson_dir / "body.md").write_text("# Problem Framing\n", encoding="utf-8")
    return lesson_dir


def _configure_tmp_content(tmp_path: Path, monkeypatch) -> tuple[Path, Path, Path]:
    curriculum_dir = tmp_path / "curriculum"
    lessons_dir = tmp_path / "lessons"
    exercises_dir = tmp_path / "exercises"
    _write_curriculum_map(curriculum_dir / "map.json")
    lesson_dir = _write_lesson(lessons_dir)
    monkeypatch.setattr(paths, "CURRICULUM_DIR", curriculum_dir)
    monkeypatch.setattr(paths, "LESSONS_DIR", lessons_dir)
    monkeypatch.setattr(paths, "EXERCISES_DIR", exercises_dir)
    monkeypatch.setitem(validate.CONTENT_DIRS, "lesson", lessons_dir)
    monkeypatch.setitem(validate.CONTENT_DIRS, "exercise", exercises_dir)
    return lessons_dir, exercises_dir, lesson_dir


def _exercise_validation_paths(lesson_json: Path, exercise_json: Path) -> tuple[str, ...]:
    return (
        str(lesson_json),
        str(exercise_json),
        "rubrics/default/*.rubric.json",
    )


def test_scaffold_level_b_exercise_under_root_and_active_solution_rule(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, exercises_dir, lesson_dir = _configure_tmp_content(tmp_path, monkeypatch)

    result = CliRunner().invoke(
        main,
        [
            "content",
            "scaffold",
            "exercise",
            "--lesson",
            "phase-01-sql-literacy-basics/reading-rows/fixture-select",
            "--level",
            "b",
            "--slug",
            "filter-visible-rows",
            "--kind",
            "query",
            "--title",
            "Filter visible rows",
        ],
    )

    assert result.exit_code == 0
    exercise_json = (
        exercises_dir
        / "phase-01-sql-literacy-basics"
        / "fixture-select"
        / "level-b"
        / "filter-visible-rows"
        / "exercise.json"
    )
    assert exercise_json.is_file()

    draft_report = validate.validate_content(
        path_globs=_exercise_validation_paths(lesson_dir / "lesson.json", exercise_json),
    )
    assert draft_report.ok

    exercise = json.loads(exercise_json.read_text(encoding="utf-8"))
    exercise["status"] = "active"
    exercise_json.write_text(json.dumps(exercise), encoding="utf-8")

    active_report = validate.validate_content(
        path_globs=_exercise_validation_paths(lesson_dir / "lesson.json", exercise_json),
    )
    assert not active_report.ok
    assert any("require solution.sql" in issue.message for issue in active_report.errors)

    (exercise_json.parent / "solution.sql").write_text("SELECT 1;\n", encoding="utf-8")
    passing_report = validate.validate_content(
        path_globs=_exercise_validation_paths(lesson_dir / "lesson.json", exercise_json),
    )
    assert passing_report.ok

    discovered_report = validate.validate_content()
    assert discovered_report.by_kind["exercise"] == 1


def test_scaffold_level_d_active_requires_three_oral_defense_prompts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, exercises_dir, lesson_dir = _configure_tmp_content(tmp_path, monkeypatch)

    result = CliRunner().invoke(
        main,
        [
            "content",
            "scaffold",
            "exercise",
            "--lesson",
            "phase-01-sql-literacy-basics/reading-rows/fixture-select",
            "--level",
            "d",
            "--slug",
            "repair-broken-query",
            "--kind",
            "debug",
            "--title",
            "Repair a broken query",
        ],
    )

    assert result.exit_code == 0
    exercise_json = (
        exercises_dir
        / "phase-01-sql-literacy-basics"
        / "fixture-select"
        / "level-d"
        / "repair-broken-query"
        / "exercise.json"
    )
    draft_report = validate.validate_content(
        path_globs=_exercise_validation_paths(lesson_dir / "lesson.json", exercise_json),
    )
    assert draft_report.ok

    exercise = json.loads(exercise_json.read_text(encoding="utf-8"))
    exercise["status"] = "active"
    exercise["oral_defense_prompts"] = ["What failed?", "How did you fix it?"]
    exercise_json.write_text(json.dumps(exercise), encoding="utf-8")

    active_report = validate.validate_content(
        path_globs=_exercise_validation_paths(lesson_dir / "lesson.json", exercise_json),
    )
    assert not active_report.ok
    assert any("at least 3 oral_defense_prompts" in issue.message for issue in active_report.errors)

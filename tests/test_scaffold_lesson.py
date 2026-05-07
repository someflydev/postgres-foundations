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
                    {
                        "number": 1,
                        "slug": "sql-literacy-basics",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_scaffold_lesson_creates_draft_and_validates(tmp_path: Path, monkeypatch) -> None:
    curriculum_dir = tmp_path / "curriculum"
    lessons_dir = tmp_path / "lessons"
    _write_curriculum_map(curriculum_dir / "map.json")
    monkeypatch.setattr(paths, "CURRICULUM_DIR", curriculum_dir)
    monkeypatch.setattr(paths, "LESSONS_DIR", lessons_dir)

    result = CliRunner().invoke(
        main,
        [
            "content",
            "scaffold",
            "lesson",
            "--phase",
            "1",
            "--cluster",
            "select-and-filter",
            "--slug",
            "first-select",
            "--title",
            "First SELECT",
            "--capability-layer",
            "schema_literacy",
        ],
    )

    assert result.exit_code == 0
    lesson_dir = lessons_dir / "phase-01-sql-literacy-basics" / "select-and-filter" / "first-select"
    lesson_json = lesson_dir / "lesson.json"
    body_md = lesson_dir / "body.md"
    assert lesson_json.is_file()
    assert body_md.is_file()

    report = validate.validate_content(path_globs=(str(lesson_json),))
    assert report.ok

    lesson = json.loads(lesson_json.read_text(encoding="utf-8"))
    lesson["status"] = "active"
    lesson_json.write_text(json.dumps(lesson), encoding="utf-8")

    active_report = validate.validate_content(path_globs=(str(lesson_json),))
    assert not active_report.ok
    assert any("__REPLACE_ME__ placeholders" in issue.message for issue in active_report.errors)


def test_scaffold_lesson_does_not_overwrite_existing_files(tmp_path: Path, monkeypatch) -> None:
    curriculum_dir = tmp_path / "curriculum"
    lessons_dir = tmp_path / "lessons"
    _write_curriculum_map(curriculum_dir / "map.json")
    monkeypatch.setattr(paths, "CURRICULUM_DIR", curriculum_dir)
    monkeypatch.setattr(paths, "LESSONS_DIR", lessons_dir)

    args = [
        "content",
        "scaffold",
        "lesson",
        "--phase",
        "1",
        "--cluster",
        "select-and-filter",
        "--slug",
        "first-select",
        "--title",
        "First SELECT",
        "--capability-layer",
        "schema_literacy",
    ]
    first = CliRunner().invoke(main, args)
    assert first.exit_code == 0

    lesson_json = (
        lessons_dir
        / "phase-01-sql-literacy-basics"
        / "select-and-filter"
        / "first-select"
        / "lesson.json"
    )
    original = lesson_json.read_text(encoding="utf-8")
    second = CliRunner().invoke(main, args)

    assert second.exit_code != 0
    assert "already contains authored files" in second.output
    assert lesson_json.read_text(encoding="utf-8") == original

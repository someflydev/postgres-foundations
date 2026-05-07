import json
from pathlib import Path

from click.testing import CliRunner

from pgfound.cli import main


def _write_lesson(path: Path, body: str, *, status: str = "active") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "id": "lint-target",
                "body_path": "body.md",
                "status": status,
            }
        ),
        encoding="utf-8",
    )
    (path.parent / "body.md").write_text(body, encoding="utf-8")


def test_lint_lesson_catches_missing_sections_short_body_and_todo(tmp_path: Path) -> None:
    lesson_json = (
        tmp_path
        / "lessons"
        / "phase-01-sql-literacy-basics"
        / "select-and-filter"
        / "lint-target"
        / "lesson.json"
    )
    _write_lesson(
        lesson_json,
        "# Problem Framing\n\nTODO: short body with https://www.postgresql.org/docs/current/sql-select.html\n",
    )

    result = CliRunner().invoke(
        main,
        ["content", "lint", "--strict", "--paths", str(lesson_json)],
    )

    assert result.exit_code != 0
    assert "active lesson body must be at least 400 words" in result.output
    assert "missing section: Minimal Concept Introduction" in result.output
    assert "active body contains TODO/TBD/XXX token" in result.output
    assert "bare URL lacks markdown title" in result.output

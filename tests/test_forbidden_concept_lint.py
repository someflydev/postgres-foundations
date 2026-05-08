import json
from pathlib import Path

from click.testing import CliRunner

from pgfound.cli import main


def test_solution_sql_using_not_yet_allowed_window_function_warns(tmp_path: Path) -> None:
    exercise_dir = (
        tmp_path
        / "exercises"
        / "phase-01-sql-literacy-basics"
        / "fixture-select"
        / "level-b"
        / "rank-customers"
    )
    exercise_dir.mkdir(parents=True)
    (exercise_dir / "exercise.json").write_text(
        json.dumps(
            {
                "id": "rank-customers",
                "lesson_id": "fixture-select",
                "not_yet_allowed_concepts": ["window_function"],
                "status": "draft",
            }
        ),
        encoding="utf-8",
    )
    (exercise_dir / "solution.sql").write_text(
        "SELECT row_number() OVER (ORDER BY id) FROM customers;\n",
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        main,
        ["content", "lint", "--paths", str(exercise_dir / "exercise.json")],
    )

    assert result.exit_code == 0
    assert "not-yet-allowed concept 'window_function'" in result.output

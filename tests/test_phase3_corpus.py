from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-03-schema-design-and-database-truth"
LEVEL_D_PATTERNS = re.compile(
    r"incident|without this constraint|could violate",
    re.IGNORECASE,
)
PLACEHOLDER_REPAIRS = re.compile(
    r"CHECK\s*\(\s*id\s*>\s*0\s*\)|required_fact_check|exact production statement",
    re.IGNORECASE,
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase3_lessons_and_exercises_validate_and_lint_cleanly() -> None:
    report = validate.validate_content(
        path_globs=(
            f"lessons/{PHASE_DIR}/**/lesson.json",
            f"exercises/{PHASE_DIR}/**/exercise.json",
            "rubrics/default/*.rubric.json",
            "curriculum/map.json",
        )
    )
    assert report.ok, [issue.message for issue in report.errors]

    lint_report = lint.lint_content(
        path_globs=(
            f"lessons/{PHASE_DIR}/**/lesson.json",
            f"exercises/{PHASE_DIR}/**/exercise.json",
        )
    )
    assert lint_report.ok, [issue.message for issue in lint_report.warnings]


def test_phase3_clusters_have_planned_lesson_count() -> None:
    curriculum = _load_json(paths.CURRICULUM_DIR / "map.json")
    phase3 = next(phase for phase in curriculum["phases"] if phase["number"] == 3)
    lessons_by_cluster: dict[str, list[Path]] = defaultdict(list)

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lessons_by_cluster[lesson_path.parent.parent.name].append(lesson_path)

    for cluster in phase3["clusters"]:
        assert len(lessons_by_cluster[cluster["slug"]]) == cluster["planned_lessons"]


def test_phase3_exercises_have_schema_checks_and_incident_language() -> None:
    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    schema_object_count = 0

    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)
        if exercise["expected_output_shape"] == "schema_object":
            schema_object_count += 1

        if exercise["scaffolding_level"] == "D":
            prompt = (exercise_path.parent / "prompt.md").read_text(encoding="utf-8")
            solution = (exercise_path.parent / exercise["solution_path"]).read_text(
                encoding="utf-8"
            )
            assert LEVEL_D_PATTERNS.search(prompt), exercise_path
            assert LEVEL_D_PATTERNS.search(solution), exercise_path
            assert not PLACEHOLDER_REPAIRS.search(solution), exercise_path

    total_exercises = sum(len(items) for items in exercises_by_lesson.values())
    assert schema_object_count >= 1
    assert total_exercises >= 65
    assert total_exercises <= 70

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        assert len(exercises_by_lesson[lesson["id"]]) >= 5


def test_phase3_lesson_specific_schema_solutions_are_not_generic() -> None:
    checks = {
        "uniqueness-beyond-primary-key": ("UNIQUE",),
        "reference-tables-over-free-text": ("REFERENCES", "FOREIGN KEY"),
        "check-constraints": ("CHECK",),
        "not-null-vs-nullable": ("SET NOT NULL",),
        "defaults-and-generated-columns": ("DEFAULT", "GENERATED ALWAYS"),
        "normalization-1nf-2nf-3nf": ("REFERENCES", "UNIQUE"),
        "refactoring-spreadsheet-shape-to-relational": ("legacy", "order_items"),
    }

    for lesson_id, required_fragments in checks.items():
        solution_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (paths.EXERCISES_DIR / PHASE_DIR / lesson_id).glob("*/*/solution.*")
        ).upper()
        for fragment in required_fragments:
            assert fragment.upper() in solution_text, (lesson_id, fragment)


def test_phase3_spreadsheet_exercise_uses_fixture_and_target_tables() -> None:
    exercise_dir = (
        paths.EXERCISES_DIR
        / PHASE_DIR
        / "refactoring-spreadsheet-shape-to-relational"
        / "level-d"
        / "refactoring-spreadsheet-shape-to-relational-diagnose-lurking-incident"
    )
    prompt = (exercise_dir / "prompt.md").read_text(encoding="utf-8")
    solution = (exercise_dir / "solution.md").read_text(encoding="utf-8")

    assert "spreadsheet-legacy.csv" in prompt
    assert "spreadsheet-legacy.csv" in solution
    for table_name in ("customers", "orders", "products", "order_items"):
        assert table_name in prompt
        assert table_name in solution

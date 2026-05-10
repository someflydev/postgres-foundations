from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-07-indexing-and-query-plans"
PHASE7A_LESSONS = {
    "sequential-scan-vs-index-lookup",
    "reading-explain-and-explain-analyze",
    "how-btree-works-in-30-minutes",
    "single-column-indexes-and-selectivity",
    "leftmost-prefix-rule",
    "column-order-matters",
    "covering-indexes",
    "write-amplification-and-bloat",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")
LESSON_REQUIRED_TERMS = {
    "sequential-scan-vs-index-lookup": ["Seq Scan", "Index Scan", "selectivity"],
    "reading-explain-and-explain-analyze": ["estimated rows", "actual rows", "buffers"],
    "how-btree-works-in-30-minutes": ["NULLS FIRST", "NULLS LAST", "INCLUDE"],
    "single-column-indexes-and-selectivity": ["low-cardinality", "customer_id", "status"],
    "leftmost-prefix-rule": ["leftmost", "(a, b, c)", "b alone"],
    "column-order-matters": ["equality first", "range", "starts_at"],
    "covering-indexes": ["Index Only Scan", "heap fetch", "INCLUDE"],
    "write-amplification-and-bloat": ["write amplification", "bloat", "vacuum"],
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase7a_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase7a_has_required_lessons_and_exercise_distribution() -> None:
    lesson_paths = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert {path.parent.name for path in lesson_paths} == PHASE7A_LESSONS
    assert len(lesson_paths) == 8

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 64
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 700
        for required_term in LESSON_REQUIRED_TERMS[lesson["id"]]:
            assert required_term in body
        assert len(exercises_by_lesson[lesson["id"]]) == 8
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_phase7a_required_drills_and_explain_references_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )
    assert exercise_text.count("pgfound lab explain") >= 6
    assert "Propose the index that matches this lesson's query pattern" in exercise_text
    assert "wrong column order" in exercise_text
    assert "bloat" in exercise_text
    assert "Phase 7b direction is a partial index" in exercise_text


def test_phase7a_level_c_solutions_are_real_index_repairs() -> None:
    generic_status_solution = "SELECT count(*)\nFROM ecommerce.orders\nWHERE status = 'paid';"
    level_c_solution_paths = sorted(
        (paths.EXERCISES_DIR / PHASE_DIR).glob("*/level-c/*/solution.sql")
    )
    assert len(level_c_solution_paths) == 16
    for solution_path in level_c_solution_paths:
        solution = solution_path.read_text(encoding="utf-8")
        assert solution.strip() != generic_status_solution
        assert "CREATE INDEX" in solution
        assert "ANALYZE" in solution

    all_solution_text = "\n".join(
        path.read_text(encoding="utf-8") for path in level_c_solution_paths
    )
    assert "INCLUDE (order_number, total_amount)" in all_solution_text
    assert "ON scheduling.appointments (provider_id, starts_at, status)" in all_solution_text
    assert "ON ecommerce.orders (customer_id, placed_at DESC)" in all_solution_text


def test_phase7a_seed_generation_contracts_are_present() -> None:
    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-07a.sql").read_text(
        encoding="utf-8"
    )
    scheduling_sql = (paths.SEED_DATA_DIR / "packs/scheduling/phases/phase-07a.sql").read_text(
        encoding="utf-8"
    )
    seed_loader = (paths.REPO_ROOT / "src/pgfound/content/seed.py").read_text(encoding="utf-8")

    assert "phase_07a_order_items_stage" in ecommerce_sql
    assert "phase_07a_appointments_stage" in scheduling_sql
    assert "generated-seed-data" in seed_loader
    assert "cursor.copy" in seed_loader

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-07-indexing-and-query-plans"
PHASE7B_LESSONS = {
    "when-partial-indexes-win",
    "the-maintenance-win",
    "functional-indexes",
    "gin-for-jsonb-and-arrays",
    "gin-cost-model",
    "gist-for-ranges-and-exclusion",
    "gist-for-geospatial-preview",
    "brin-for-append-heavy-chronological-data",
    "explain-analyze-deep-dive",
    "plan-debugging-workflow",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")
REQUIRED_TEXT = {
    "when-partial-indexes-win": ["partial index", "status = 'pending'", "predicate"],
    "functional-indexes": ["lower(email)", "date_trunc"],
    "gin-for-jsonb-and-arrays": ["jsonb_path_ops", "jsonb_ops", "array membership"],
    "gin-cost-model": ["fastupdate", "pending list", "bloat"],
    "gist-for-ranges-and-exclusion": ["exclusion constraint", "&&"],
    "brin-for-append-heavy-chronological-data": ["BRIN", "physical correlation"],
    "explain-analyze-deep-dive": ["estimated rows", "actual rows", "CREATE STATISTICS"],
    "plan-debugging-workflow": ["EXPLAIN ANALYZE BUFFERS", "hypothesize", "measure"],
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _phase7b_lesson_paths() -> list[Path]:
    return [
        path
        for path in sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
        if path.parent.name in PHASE7B_LESSONS
    ]


def test_phase7b_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase7b_has_required_lessons_and_distribution() -> None:
    lesson_paths = _phase7b_lesson_paths()
    assert {path.parent.name for path in lesson_paths} == PHASE7B_LESSONS
    assert len(lesson_paths) == 10

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        if exercise["lesson_id"] in PHASE7B_LESSONS:
            exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 80
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 700
        for required in REQUIRED_TEXT.get(lesson["id"], []):
            assert required in body
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_phase7b_required_drills_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )

    assert "WHERE status = 'pending'" in exercise_text
    assert "lower(email) = lower" in exercise_text
    assert "payload @>" in exercise_text
    assert "USING gist" in exercise_text
    assert "USING brin" in exercise_text
    assert "bloat-to-value ratio" in exercise_text
    assert "CREATE STATISTICS" in exercise_text


def test_phase7b_docs_and_seed_extensions_are_present() -> None:
    assert (paths.REPO_ROOT / "docs/indexing-playbook-part2.md").is_file()
    assert (paths.REPO_ROOT / "docs/anti-patterns/unused_indexes.md").is_file()
    assert (paths.REPO_ROOT / "docs/anti-patterns/redundant_indexes.md").is_file()

    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-07b.sql").read_text(
        encoding="utf-8"
    )
    event_sql = (paths.SEED_DATA_DIR / "packs/event_heavy_ops/phases/phase-07b.sql").read_text(
        encoding="utf-8"
    )

    assert "delivered" in ecommerce_sql
    assert "pending" in ecommerce_sql
    assert "payload" in event_sql
    assert "severity" in event_sql

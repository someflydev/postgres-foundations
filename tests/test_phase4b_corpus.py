from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-04-postgresql-data-modeling"
PHASE4B_LESSONS = {
    "what-arrays-are-good-for",
    "what-arrays-are-bad-for",
    "querying-arrays",
    "arrays-and-indexing-preview",
    "what-a-range-is",
    "range-operators",
    "exclusion-constraints",
    "what-multiranges-unlock",
    "operations-on-multiranges",
    "ranges-vs-arrays-vs-child-tables",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _phase4b_lesson_paths() -> list[Path]:
    return [
        path
        for path in sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
        if _load_json(path)["id"] in PHASE4B_LESSONS
    ]


def test_phase4b_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase4b_has_required_lessons_and_exercise_distribution() -> None:
    lessons = _phase4b_lesson_paths()
    assert {path.parent.name for path in lessons} == PHASE4B_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        if exercise["lesson_id"] in PHASE4B_LESSONS:
            exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 70
    for lesson_path in lessons:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 500
        assert "good-fit" in body.lower()
        assert "bad-fit" in body.lower()
        assert len(exercises_by_lesson[lesson["id"]]) == 7


def test_phase4b_required_drills_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )
    assert "EXCLUDE USING gist" in exercise_text
    assert "conflicting key value rejected" in exercise_text
    assert "roles text[]" in exercise_text
    assert "starts_at` and `ends_at" in exercise_text
    assert "total unavailability in the next 7 days" in exercise_text
    assert "tstzmultirange" in exercise_text


def test_phase4b_domain_sql_and_antipattern_doc_exist() -> None:
    for domain in ("ecommerce", "scheduling", "event_heavy_ops"):
        assert (paths.SEED_DATA_DIR / "packs" / domain / "phases" / "phase-04b.sql").is_file()

    antipattern = paths.REPO_ROOT / "docs" / "anti-patterns" / "arrays_over_child_tables.md"
    doctrine = paths.REPO_ROOT / "docs" / "doctrine.md"
    cookbook = paths.REPO_ROOT / "docs" / "constraints-cookbook.md"
    assert antipattern.is_file()
    assert "anti-patterns/arrays_over_child_tables.md" in doctrine.read_text(encoding="utf-8")
    assert "EXCLUDE USING gist" in cookbook.read_text(encoding="utf-8")


def test_phase4b_domain_sql_matches_prompt_schema_contracts() -> None:
    ecommerce_sql = (
        paths.SEED_DATA_DIR / "packs" / "ecommerce" / "phases" / "phase-04b.sql"
    ).read_text(encoding="utf-8")
    scheduling_sql = (
        paths.SEED_DATA_DIR / "packs" / "scheduling" / "phases" / "phase-04b.sql"
    ).read_text(encoding="utf-8")
    events_sql = (
        paths.SEED_DATA_DIR / "packs" / "event_heavy_ops" / "phases" / "phase-04b.sql"
    ).read_text(encoding="utf-8")

    assert "ADD COLUMN IF NOT EXISTS tags text[]" in ecommerce_sql
    assert "CREATE TABLE IF NOT EXISTS ecommerce.price_history" in ecommerce_sql
    assert "price_history numrange" not in ecommerce_sql
    assert "ADD COLUMN IF NOT EXISTS working_hours tstzmultirange" in scheduling_sql
    assert "CREATE TABLE IF NOT EXISTS scheduling.availability_slots" in scheduling_sql
    assert "CREATE TABLE IF NOT EXISTS events.event_windows" in events_sql
    assert "USING gist" in events_sql

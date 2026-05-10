from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-04-postgresql-data-modeling"
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase4a_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase4a_has_required_lessons_and_exercise_distribution() -> None:
    lessons = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert len(lessons) == 9

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 63
    for lesson_path in lessons:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 500
        assert "good-fit" in body.lower()
        assert "bad-fit" in body.lower()
        assert len(exercises_by_lesson[lesson["id"]]) == 7


def test_phase4a_jsonb_lessons_reference_antipattern_doc() -> None:
    referenced = []
    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        concepts = set(lesson.get("concepts_introduced", []))
        if "jsonb" not in concepts:
            continue
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        refs = {ref["slug"] for ref in lesson.get("references", [])}
        referenced.append("jsonb-everything" in refs or "jsonb_everything.md" in body)
    assert referenced
    assert all(referenced)


def test_phase4a_required_level_d_drills_are_present() -> None:
    phase_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/prompt.md")
    )
    assert "timezone-naive timestamp" in phase_text
    assert "metadata ->> 'channel'" in phase_text
    assert "wrong index" in phase_text

    jsonb_index_exercise = _load_json(
        paths.EXERCISES_DIR
        / PHASE_DIR
        / "querying-jsonb"
        / "level-d"
        / "querying-jsonb-diagnose-phase4a-incident"
        / "exercise.json"
    )
    assert "gin_index" in jsonb_index_exercise["not_yet_allowed_concepts"]


def test_phase4a_domain_sql_and_antipattern_doc_exist() -> None:
    for domain in ("ecommerce", "scheduling", "saas_multi_tenant"):
        assert (
            paths.SEED_DATA_DIR / "packs" / domain / "phases" / "phase-04a.sql"
        ).is_file()

    antipattern = paths.REPO_ROOT / "docs" / "anti-patterns" / "jsonb_everything.md"
    doctrine = paths.REPO_ROOT / "docs" / "doctrine.md"
    assert antipattern.is_file()
    assert "anti-patterns/jsonb_everything.md" in doctrine.read_text(encoding="utf-8")


def test_phase4a_domain_sql_matches_prompt_schema_contracts() -> None:
    scheduling_sql = (
        paths.SEED_DATA_DIR
        / "packs"
        / "scheduling"
        / "phases"
        / "phase-04a.sql"
    ).read_text(encoding="utf-8")
    saas_sql = (
        paths.SEED_DATA_DIR
        / "packs"
        / "saas_multi_tenant"
        / "phases"
        / "phase-04a.sql"
    ).read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS scheduling.professionals" in scheduling_sql
    assert "professionals_timezone_valid_check" in scheduling_sql
    assert "RENAME COLUMN uuid_id TO id" in saas_sql
    assert "ADD CONSTRAINT users_pkey PRIMARY KEY (id)" in saas_sql

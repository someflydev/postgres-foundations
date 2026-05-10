from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-08-postgresql-full-text-search"
PHASE8_LESSONS = {
    "why-lexical-search-first",
    "tsvector-and-tsquery",
    "parsers-and-dictionaries",
    "plainto-websearch-to-tsquery",
    "indexing-fts-with-gin",
    "stored-vs-generated-tsvector",
    "weighted-search-and-ranking",
    "headlines-and-snippets",
    "multi-language-and-unaccent",
    "when-to-leave-core-fts",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase8_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase8_has_required_lessons_and_exercise_distribution() -> None:
    lesson_paths = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert {path.parent.name for path in lesson_paths} == PHASE8_LESSONS
    assert len(lesson_paths) == 10

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 80
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        levels = [
            exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]
        ]
        assert len(WORD_RE.findall(body)) >= 400
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_phase8_required_references_and_drills_are_present() -> None:
    content_text = "\n".join(
        path.read_text(encoding="utf-8")
        for base in (paths.LESSONS_DIR / PHASE_DIR, paths.EXERCISES_DIR / PHASE_DIR)
        for path in base.glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )
    assert "pg_trgm" in content_text
    assert "pgvector" in content_text
    assert "title=A, brand=B, description=C" in content_text
    assert "ILIKE '%pattern%'" in content_text
    assert "hyphenated term" in content_text
    assert "trigger-maintained tsvector silently goes stale" in content_text


def test_phase8_seed_and_docs_wire_unaccent_and_search_vectors() -> None:
    initdb = (paths.REPO_ROOT / "docker/initdb/00-extensions.sql").read_text(encoding="utf-8")
    doc_sql = (paths.SEED_DATA_DIR / "packs/document_search/phases/phase-08.sql").read_text(
        encoding="utf-8"
    )
    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-08.sql").read_text(
        encoding="utf-8"
    )
    playbook = (paths.REPO_ROOT / "docs/search-playbook.md").read_text(encoding="utf-8")

    assert "CREATE EXTENSION IF NOT EXISTS unaccent" in initdb
    assert "documents.docs" in doc_sql
    assert "GENERATED ALWAYS" in doc_sql
    assert "USING gin (search_vec)" in doc_sql
    assert "generate_series(1, 5000)" in doc_sql
    assert "product_search_vec" in ecommerce_sql
    assert "pg_trgm" in playbook
    assert "pgvector" in playbook

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

E1 = "e1-pg-stat-statements"
E2 = "e2-pg-trgm"
E1_LESSONS = {
    "what-pg-stat-statements-actually-captures",
    "installation-and-configuration",
    "reset-discipline-and-baselines",
    "triage-patterns",
    "integrating-with-explain-workflows",
    "cost-and-caveats",
}
E2_LESSONS = {
    "what-pg-trgm-is-for",
    "similarity-and-word-similarity",
    "gin-and-gist-on-trigrams",
    "combining-fts-and-trigrams",
    "deduplication-candidates",
    "support-ui-search",
    "cost-and-caveats",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_extension_e1_e2_validate_and_lint_cleanly() -> None:
    report = validate.validate_content(
        path_globs=(
            "curriculum/extensions/map.json",
            "lessons/extensions/**/*.json",
            "exercises/extensions/**/*.json",
            "rubrics/default/*.rubric.json",
        )
    )
    assert report.ok, [f"{issue.path}: {issue.message}" for issue in report.errors]

    lint_report = lint.lint_content(
        path_globs=("lessons/extensions/**/*.json", "exercises/extensions/**/*.json")
    )
    assert lint_report.ok, [f"{issue.path}: {issue.message}" for issue in lint_report.warnings]


def test_extension_e1_e2_lessons_and_distribution() -> None:
    e1_paths = sorted((paths.LESSONS_DIR / "extensions" / E1).glob("*/lesson.json"))
    e2_paths = sorted((paths.LESSONS_DIR / "extensions" / E2).glob("*/lesson.json"))
    assert {path.parent.name for path in e1_paths} == E1_LESSONS
    assert {path.parent.name for path in e2_paths} == E2_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / "extensions").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    lesson_ids = []
    for lesson_path in e1_paths + e2_paths:
        lesson_ids.append(_load(lesson_path)["id"])

    assert sum(len(exercises_by_lesson[lesson_id]) for lesson_id in lesson_ids) == 104

    for lesson_path in e1_paths + e2_paths:
        lesson = _load(lesson_path)
        assert lesson["module_id"] == lesson_path.parent.parent.name
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 400
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_extension_critical_drills_and_docs_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "extensions").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    assert "top regression after a fictional deploy" in exercise_text
    assert "pg_stat_statements.max is too low" in exercise_text
    assert "word_similarity() and justify a sensible threshold" in exercise_text
    assert "LIKE 'prefix%'" in exercise_text
    assert "btree expression index" in exercise_text

    assert (paths.REPO_ROOT / "docs/extension-track/README.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/e1-pg-stat-statements.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/e2-pg-trgm.md").is_file()
    search_playbook = (paths.REPO_ROOT / "docs/search-playbook.md").read_text(encoding="utf-8")
    assert "docs/extension-track/e2-pg-trgm.md" in search_playbook


def test_pg_trgm_enabled_in_initdb() -> None:
    init_sql = (paths.REPO_ROOT / "docker/initdb/00-extensions.sql").read_text(encoding="utf-8")
    assert "CREATE EXTENSION IF NOT EXISTS pg_trgm;" in init_sql

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

E5 = "e5-timescaledb"
E6 = "e6-postgres-fdw"
E5_LESSONS = {
    "timescale-what-it-is",
    "creating-a-hypertable",
    "continuous-aggregates",
    "compression-and-downsampling",
    "retention-policies",
    "query-patterns-that-win",
    "operational-posture",
    "when-core-partitioning-is-enough",
    "migrating-to-timescale",
}
E6_LESSONS = {
    "predicate-pushdown-fundamentals",
    "join-pushdown-and-aggregate-pushdown",
    "async-append-for-fdw",
    "foreign-table-statistics",
    "authentication-patterns",
    "reliability-modes",
    "pushdown-trips-and-rewrites",
    "from-fdw-to-logical-replication",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_extension_e5_e6_validate_and_lint_cleanly() -> None:
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


def test_extension_e5_e6_lessons_and_distribution() -> None:
    e5_paths = sorted((paths.LESSONS_DIR / "extensions" / E5).glob("*/lesson.json"))
    e6_paths = sorted((paths.LESSONS_DIR / "extensions" / E6).glob("*/lesson.json"))
    assert {path.parent.name for path in e5_paths} == E5_LESSONS
    assert {path.parent.name for path in e6_paths} == E6_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / "extensions").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    lesson_ids = [_load(path)["id"] for path in e5_paths + e6_paths]
    assert sum(len(exercises_by_lesson[lesson_id]) for lesson_id in lesson_ids) == 136

    for lesson_path in e5_paths + e6_paths:
        lesson = _load(lesson_path)
        assert lesson["module_id"] == lesson_path.parent.parent.name
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 400
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_extension_e5_e6_critical_drills_and_docs_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "extensions").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    assert "hypertable + continuous aggregate; compare query times" in exercise_text
    assert "compression policy that silently prevents updates to historical rows" in exercise_text
    assert "EXPLAIN VERBOSE showing the pushdown" in exercise_text
    assert "aggregate query that does not push down due to a non-pushable function" in exercise_text
    assert "pg_sleep trigger or similar" in exercise_text
    assert "timeout/circuit-breaker pattern at the app layer" in exercise_text

    assert (paths.REPO_ROOT / "docs/extension-track/e5-timescaledb.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/e6-postgres-fdw.md").is_file()
    assert (paths.REPO_ROOT / "docs/anti-patterns/timescale_too_early.md").is_file()

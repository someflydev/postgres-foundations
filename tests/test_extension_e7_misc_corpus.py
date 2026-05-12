from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

MODULE_LESSONS = {
    "e7-citus": {
        "citus-what-it-is",
        "distribution-key-discipline",
        "reference-tables-vs-distributed-tables",
        "co-located-joins-and-why-they-matter",
        "multi-tenant-via-citus",
        "real-time-analytics-via-citus",
        "operational-cost-of-citus",
        "citus-on-managed-services",
        "moving-to-citus-from-a-single-node",
        "when-not-to-adopt-citus",
    },
    "ltree": {
        "what-ltree-is-for",
        "alternatives-to-ltree",
        "gist-and-gin-indexes-on-ltree",
        "ltree-operators",
        "when-not-to-use-ltree",
    },
    "pg-partman": {
        "what-pg-partman-adds",
        "configuring-parent-tables",
        "operational-rhythm",
        "migrating-from-manual-partitioning",
        "when-pg-partman-is-enough-and-when-to-go-further",
    },
    "pgbouncer": {
        "pool-modes-revisited",
        "pgbouncer-config-surface",
        "pgbouncer-with-scram",
        "pgbouncer-and-prepared-statements",
        "observability-of-pgbouncer",
        "when-pgbouncer-is-not-enough",
    },
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_extension_e7_misc_validate_and_lint_cleanly() -> None:
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


def test_extension_e7_misc_lessons_and_distribution() -> None:
    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / "extensions").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    lesson_ids: list[str] = []
    for module_id, expected_lessons in MODULE_LESSONS.items():
        lesson_paths = sorted((paths.LESSONS_DIR / "extensions" / module_id).glob("*/lesson.json"))
        assert {path.parent.name for path in lesson_paths} == expected_lessons
        for lesson_path in lesson_paths:
            lesson = _load(lesson_path)
            lesson_ids.append(lesson["id"])
            assert lesson["module_id"] == module_id
            body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
            assert len(WORD_RE.findall(body)) >= 400
            levels = [
                exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]
            ]
            assert levels.count("A") == 2
            assert levels.count("B") == 2
            assert levels.count("C") == 2
            assert levels.count("D") == 2

    assert sum(len(exercises_by_lesson[lesson_id]) for lesson_id in lesson_ids) == 208


def test_extension_e7_misc_critical_drills_and_docs_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "extensions").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    assert "propose a distribution key" in exercise_text
    assert "citus_orders" in exercise_text
    assert "customer_id" in exercise_text
    assert "tenant_id" not in exercise_text
    assert "broadcast that explodes" in exercise_text
    assert "query ancestors and descendants" in exercise_text
    assert "Migrate the phase-09 manual partitioning scheme onto pg_partman" in exercise_text
    assert "Transaction-pooling breaks session-scoped LISTEN/NOTIFY" in exercise_text

    assert (paths.REPO_ROOT / "docs/extension-track/e7-citus.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/ltree.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/pg_partman.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/pgbouncer.md").is_file()
    assert (paths.REPO_ROOT / "docs/anti-patterns/shard_without_distribution_key.md").is_file()

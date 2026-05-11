from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-09-partitioning-and-large-table-operations"
PHASE9_LESSONS = {
    "what-problem-partitioning-solves",
    "range-list-hash",
    "declarative-partitioning-basics",
    "partition-pruning-and-plan-reading",
    "indexes-on-partitioned-tables",
    "uniqueness-on-partitioned-tables",
    "attach-and-detach-lifecycle",
    "pg-partman-preview",
    "when-not-to-partition",
    "operational-checklist",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase9_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase9_has_required_lessons_and_exercise_distribution() -> None:
    lesson_paths = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert {path.parent.name for path in lesson_paths} == PHASE9_LESSONS
    assert len(lesson_paths) == 10

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 80
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert len(WORD_RE.findall(body)) >= 400
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_phase9_required_drills_and_premature_language_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )

    assert "create a range-partitioned events table" in exercise_text.lower()
    assert "confirm pruning via EXPLAIN" in exercise_text
    assert "DETACH" in exercise_text
    assert "function to the partition key" in exercise_text
    assert "silently allow duplicates across partitions" in exercise_text
    assert re.search(r"\b(premature|too early)\b", exercise_text, re.IGNORECASE)


def test_phase9_docs_and_seed_extensions_are_present() -> None:
    event_sql = (paths.SEED_DATA_DIR / "packs/event_heavy_ops/phases/phase-09.sql").read_text(
        encoding="utf-8"
    )
    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-09.sql").read_text(
        encoding="utf-8"
    )
    playbook = (paths.REPO_ROOT / "docs/partitioning-playbook.md").read_text(encoding="utf-8")
    anti_pattern = (paths.REPO_ROOT / "docs/anti-patterns/partition_too_early.md").read_text(
        encoding="utf-8"
    )
    indexing = (paths.REPO_ROOT / "docs/indexing-playbook-part2.md").read_text(encoding="utf-8")

    assert "events.event_log_partitioned" in event_sql
    assert "PARTITION BY RANGE (event_time)" in event_sql
    assert event_sql.count("PARTITION OF events.event_log_partitioned") == 13
    assert "generate_series(1, 1000008)" in event_sql
    assert "USING brin (event_time)" in event_sql
    assert "DETACH PARTITION events.event_log_partitioned_2025_05" in event_sql
    assert "ecommerce.orders_partitioned" in ecommerce_sql
    assert "PARTITION BY RANGE (ordered_at)" in ecommerce_sql
    assert "unique constraints on partitioned parents must include the partition key" in indexing
    assert "Retention Template" in playbook
    assert "row count alone is not enough" in anti_pattern

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

A5 = "a5-monitoring-and-performance-ops"
A6 = "a6-replication-and-ha"
A5_LESSONS = {
    "pg-stat-statements-operationally",
    "pg-stat-activity-and-blocking",
    "index-usage-and-unused-indexes",
    "slow-query-triage-workflow",
    "growth-and-capacity",
    "wait-events-intro",
    "metrics-to-export",
    "alerting-with-context",
}
A6_LESSONS = {
    "replica-concepts-recap",
    "replica-lag-monitoring",
    "read-replica-routing",
    "failover-basics",
    "promoting-a-replica",
    "logical-replication-lifecycle-in-ops",
    "logical-replication-failure-modes",
    "upgrade-via-logical-replication",
    "postmortem-discipline",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")

REQUIRED_TEXT = {
    "pg-stat-statements-operationally": ["pg_stat_statements", "top 5 by total time"],
    "pg-stat-activity-and-blocking": ["pg_locks", "pg_blocking_pids()", "who is blocking whom"],
    "slow-query-triage-workflow": ["EXPLAIN (ANALYZE, BUFFERS)", "pg_stat_user_tables"],
    "metrics-to-export": ["checkpoints", "bgwriter", "WAL generation"],
    "replica-lag-monitoring": ["pg_wal_lsn_diff", "byte lag", "time lag"],
    "promoting-a-replica": ["pg_promote()", "old primary is fenced"],
    "logical-replication-failure-modes": ["replica identity", "schema drift"],
    "postmortem-discipline": ["invariant violated", "blast radius", "detection latency"],
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_admin_a5_a6_validate_and_lint_cleanly() -> None:
    report = validate.validate_content(
        path_globs=(
            "curriculum/admin/map.json",
            "lessons/admin/**/*.json",
            "exercises/admin/**/*.json",
            "rubrics/default/*.rubric.json",
        )
    )
    assert report.ok, [issue.message for issue in report.errors]

    lint_report = lint.lint_content(
        path_globs=("lessons/admin/**/*.json", "exercises/admin/**/*.json")
    )
    assert lint_report.ok, [issue.message for issue in lint_report.warnings]


def test_admin_a5_a6_lessons_and_exercise_distribution() -> None:
    a5_paths = sorted((paths.LESSONS_DIR / "admin" / A5).glob("*/lesson.json"))
    a6_paths = sorted((paths.LESSONS_DIR / "admin" / A6).glob("*/lesson.json"))
    assert {path.parent.name for path in a5_paths} == A5_LESSONS
    assert {path.parent.name for path in a6_paths} == A6_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / "admin").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(exercises_by_lesson[lesson]) for lesson in A5_LESSONS | A6_LESSONS) == 136

    for lesson_path in a5_paths + a6_paths:
        lesson = _load(lesson_path)
        assert lesson["module_id"] == lesson_path.parent.parent.name
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 400
        for phrase in REQUIRED_TEXT.get(lesson["id"], []):
            assert phrase in body
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_admin_a5_a6_critical_drills_docs_and_monitoring_scripts_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "admin").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    assert "weekly triage report from pg_stat_statements" in exercise_text
    assert "reproduce a blocking chain" in exercise_text
    assert "compute replication lag in bytes and time" in exercise_text
    assert "0 byte lag scenario that is still wrong" in exercise_text
    assert "noisy alert rule that fires on normal checkpoint spikes" in exercise_text

    assert (paths.REPO_ROOT / "docs/admin-track/a5-monitoring-playbook.md").is_file()
    assert (paths.REPO_ROOT / "docs/admin-track/a6-replication-ha-playbook.md").is_file()
    assert (paths.REPO_ROOT / "docs/postmortem-template.md").is_file()

    monitoring_dir = paths.REPO_ROOT / "scripts/monitoring"
    assert {path.name for path in monitoring_dir.glob("*.sql")} == {
        "top-by-total-time.sql",
        "blocking-chain.sql",
        "unused-indexes.sql",
        "replica-lag.sql",
        "table-sizes.sql",
    }

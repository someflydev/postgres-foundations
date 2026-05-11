from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

A3 = "a3-auth-and-pooling"
A4 = "a4-maintenance-and-lifecycle"
A3_LESSONS = {
    "pg-hba-concepts",
    "auth-methods-overview",
    "rotating-credentials-and-secret-management",
    "connection-hygiene",
    "pooling-intro",
    "pgbouncer-primer",
    "ssl-and-certificates",
    "connection-storm-survival",
}
A4_LESSONS = {
    "logical-vs-physical-backups",
    "pg-dump-in-practice",
    "pg-basebackup-and-point-in-time-recovery",
    "restore-drills-are-mandatory",
    "autovacuum-in-30-minutes",
    "bloat-and-how-to-see-it",
    "manual-vacuum-and-when-it-is-needed",
    "statistics-freshness",
    "major-version-upgrades",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")

REQUIRED_TEXT = {
    "pg-hba-concepts": ["pg_hba_file_rules", "hostssl", "first matching rule wins"],
    "auth-methods-overview": ["scram-sha-256", "SCRAM over md5"],
    "pooling-intro": ["transaction pooling", "prepared statements"],
    "pgbouncer-primer": ["PgBouncer", "application layer multiplexing"],
    "logical-vs-physical-backups": ["pg_dump", "pg_basebackup", "WAL archive"],
    "restore-drills-are-mandatory": ["restore drill", "known-good query"],
    "autovacuum-in-30-minutes": ["xmin horizon", "autovacuum"],
    "statistics-freshness": ["ANALYZE", "bad index scan"],
    "major-version-upgrades": ["pg_upgrade", "logical replication"],
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_admin_a3_a4_validate_and_lint_cleanly() -> None:
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


def test_admin_a3_a4_lessons_exercises_and_restore_drill_tag() -> None:
    a3_paths = sorted((paths.LESSONS_DIR / "admin" / A3).glob("*/lesson.json"))
    a4_paths = sorted((paths.LESSONS_DIR / "admin" / A4).glob("*/lesson.json"))
    assert {path.parent.name for path in a3_paths} == A3_LESSONS
    assert {path.parent.name for path in a4_paths} == A4_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    restore_drills = []
    for exercise_path in (paths.EXERCISES_DIR / "admin").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)
        if exercise.get("restore_drill") is True:
            restore_drills.append(exercise)

    assert sum(len(exercises_by_lesson[lesson]) for lesson in A3_LESSONS | A4_LESSONS) == 136
    assert any(
        exercise["lesson_id"] == "restore-drills-are-mandatory" for exercise in restore_drills
    )

    for lesson_path in a3_paths + a4_paths:
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


def test_admin_a3_a4_critical_drills_docs_and_script_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "admin").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    assert "requires SCRAM for app_scram_user" in exercise_text
    assert "scripts/restore-drill.sh" in exercise_text
    assert "long-running transaction holding the xmin horizon" in exercise_text
    assert "bad index scan after a bulk load" in exercise_text
    assert "transaction pooling breaking SET state and prepared statements" in exercise_text

    assert (paths.REPO_ROOT / "docs/admin-track/a3-auth-and-pooling-playbook.md").is_file()
    assert (paths.REPO_ROOT / "docs/admin-track/a4-backup-and-upgrades-playbook.md").is_file()
    assert (paths.REPO_ROOT / "scripts/restore-drill.sh").is_file()

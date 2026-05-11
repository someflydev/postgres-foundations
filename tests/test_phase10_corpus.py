from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-10-roles-rls-replication-and-fdw"
PHASE10_LESSONS = {
    "login-vs-group-roles-and-membership",
    "grants-on-tables-schemas-sequences-functions",
    "default-privileges",
    "ownership-and-object-hierarchy",
    "introduction-to-row-level-security",
    "authoring-policies",
    "rls-performance-and-indexing",
    "physical-replication-concepts",
    "logical-replication-basics",
    "logical-replication-lab",
    "postgres-fdw-introduction",
    "modernization-bridge-pattern",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase10_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase10_has_required_lessons_and_exercise_distribution() -> None:
    lesson_paths = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert {path.parent.name for path in lesson_paths} == PHASE10_LESSONS
    assert len(lesson_paths) == 12

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 96
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert len(WORD_RE.findall(body)) >= 400
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_phase10_required_drills_and_docs_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )
    saas_sql = (paths.SEED_DATA_DIR / "packs/saas_multi_tenant/phases/phase-10.sql").read_text(
        encoding="utf-8"
    )
    bridge_sql = (paths.SEED_DATA_DIR / "packs/modernization_bridge/phases/phase-10.sql").read_text(
        encoding="utf-8"
    )
    lab = (paths.REPO_ROOT / "docs/lab.md").read_text(encoding="utf-8")

    assert "SET app.tenant_id" in saas_sql
    assert "ENABLE ROW LEVEL SECURITY" in saas_sql
    assert "FORCE ROW LEVEL SECURITY" in saas_sql
    assert "postgres_fdw" in bridge_sql
    assert "IMPORT FOREIGN SCHEMA legacy" in bridge_sql
    assert "pg-replica" in lab
    assert "cross-tenant queries return 0 rows" in exercise_text
    assert "publication on pg and a subscription on pg-replica" in exercise_text
    assert "USING (true)" in exercise_text
    assert "unvacuumable catalog table" in exercise_text
    assert "predicate is not pushed down" in exercise_text


def test_phase10_lesson_bodies_are_topic_specific() -> None:
    bodies = [
        path.read_text(encoding="utf-8")
        for path in sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/body.md"))
    ]

    assert len(bodies) == 12
    assert not any("Phase 10 treats" in body for body in bodies)
    assert len(set(bodies)) == 12

    required_phrases = {
        "Login vs Group Roles and Membership": "permission graph",
        "Authoring Policies": "WITH CHECK",
        "Logical Replication Lab": "host=pg",
        "Modernization Bridge Pattern": "unmapped-data report",
    }
    joined = "\n".join(bodies)
    for title, phrase in required_phrases.items():
        assert title in joined
        assert phrase in joined

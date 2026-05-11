from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

A1 = "a1-roles-and-privileges"
A2 = "a2-schemas-and-databases"
A1_LESSONS = {
    "roles-vs-users",
    "login-roles-and-group-roles",
    "granting-on-tables-sequences-functions-schemas",
    "default-privileges",
    "membership-and-inheritance",
    "ownership-and-dependent-objects",
    "least-privilege-patterns",
    "auditing-privileges-and-reviewing-access",
}
A2_LESSONS = {
    "what-a-schema-is-for",
    "schemas-vs-databases",
    "public-schema-discipline",
    "search-path-discipline",
    "multi-tenant-via-schemas-vs-rls",
    "migrating-between-schemas-and-databases",
    "cluster-level-management-basics",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")
FORBIDDEN_REFERENCES = (
    "information_schema.schema_privileges",
    "supplied grant or schema fragment",
    "Keep the answer specific",
)
REQUIRED_BODY_PHRASES = {
    "roles-vs-users": ["LOGIN", "NOLOGIN", "one object kind"],
    "login-roles-and-group-roles": ["NOLOGIN group roles", "app_api_login"],
    "granting-on-tables-sequences-functions-schemas": ["sequence", "function EXECUTE"],
    "default-privileges": ["future objects", "does not repair existing objects"],
    "membership-and-inheritance": ["NOINHERIT", "SET ROLE", "current_user"],
    "ownership-and-dependent-objects": ["REASSIGN OWNED", "dependent objects"],
    "least-privilege-patterns": ["role matrix", "break-glass"],
    "auditing-privileges-and-reviewing-access": ["pg_auth_members", "aclexplode"],
    "what-a-schema-is-for": ["namespace", "search_path"],
    "schemas-vs-databases": ["one database with many schemas", "lifecycle"],
    "public-schema-discipline": ["PostgreSQL 15", "REVOKE CREATE"],
    "search-path-discipline": ["SECURITY DEFINER", "pg_catalog, saas"],
    "multi-tenant-via-schemas-vs-rls": ["schema-per-tenant", "RLS"],
    "migrating-between-schemas-and-databases": ["pg_dump", "logical replication"],
    "cluster-level-management-basics": ["CREATE DATABASE", "LC_COLLATE", "LC_CTYPE"],
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_admin_a1_a2_validate_and_lint_cleanly() -> None:
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


def test_admin_a1_a2_lessons_and_distribution() -> None:
    a1_paths = sorted((paths.LESSONS_DIR / "admin" / A1).glob("*/lesson.json"))
    a2_paths = sorted((paths.LESSONS_DIR / "admin" / A2).glob("*/lesson.json"))
    assert {path.parent.name for path in a1_paths} == A1_LESSONS
    assert {path.parent.name for path in a2_paths} == A2_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / "admin").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 120
    bodies = []
    for lesson_path in a1_paths + a2_paths:
        lesson = _load(lesson_path)
        assert lesson["module_id"] == lesson_path.parent.parent.name
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        bodies.append(body)
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert len(WORD_RE.findall(body)) >= 700
        for phrase in REQUIRED_BODY_PHRASES[lesson["id"]]:
            assert phrase in body
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2
    assert len(set(bodies)) == len(bodies)


def test_admin_a1_a2_content_has_no_invalid_references_or_generic_prompts() -> None:
    admin_text = "\n".join(
        path.read_text(encoding="utf-8")
        for root in (
            paths.LESSONS_DIR / "admin",
            paths.EXERCISES_DIR / "admin",
            paths.REPO_ROOT / "docs/admin-track",
            paths.SEED_DATA_DIR / "packs/admin",
        )
        for path in root.glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    for forbidden in FORBIDDEN_REFERENCES:
        assert forbidden not in admin_text

    for prompt_path in (paths.EXERCISES_DIR / "admin").glob("**/prompt.md"):
        prompt = prompt_path.read_text(encoding="utf-8")
        starter = (prompt_path.parent / "starter.sql").read_text(encoding="utf-8")
        assert "## Scenario" in prompt
        assert len(WORD_RE.findall(prompt)) >= 20
        assert len(starter.strip().splitlines()) >= 2


def test_admin_required_drills_seed_pack_and_docs_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "admin").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    roles_sql = (paths.SEED_DATA_DIR / "packs/admin/roles-matrix.sql").read_text(encoding="utf-8")
    review_sql = (paths.SEED_DATA_DIR / "packs/admin/access-review-queries.sql").read_text(
        encoding="utf-8"
    )

    assert "least-privilege role matrix for the saas domain" in exercise_text
    assert "leaked role audit" in exercise_text
    assert "REVOKE CREATE ON SCHEMA public FROM PUBLIC" in exercise_text
    assert "SET search_path = pg_catalog, saas" in exercise_text
    assert "CREATE ROLE saas_app_readwrite NOLOGIN" in roles_sql
    assert "information_schema.table_privileges" in review_sql
    assert (paths.REPO_ROOT / "docs/admin-track/README.md").is_file()
    assert (paths.REPO_ROOT / "docs/admin-track/a1-roles-playbook.md").is_file()
    assert (paths.REPO_ROOT / "docs/admin-track/a2-schemas-playbook.md").is_file()

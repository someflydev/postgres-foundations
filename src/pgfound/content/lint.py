"""Authoring lint checks for content."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from pgfound.content import validate

SECTION_TITLES: Final[tuple[str, ...]] = (
    "Problem Framing",
    "Minimal Concept Introduction",
    "Worked Example",
    "Diagnostic Questions",
    "Common Pitfalls",
    "Explain It Back",
    "References and Further Reading",
)
BARE_URL_RE: Final[re.Pattern[str]] = re.compile(r"(?<!\]\()https?://[^\s)]+")
TODO_RE: Final[re.Pattern[str]] = re.compile(r"\b(TODO|TBD|XXX)\b", re.IGNORECASE)
WORD_RE: Final[re.Pattern[str]] = re.compile(r"\b[\w'-]+\b")
FORBIDDEN_SQL_PATTERNS: Final[dict[str, tuple[re.Pattern[str], ...]]] = {
    "window_function": (re.compile(r"\bOVER\s*\(", re.IGNORECASE),),
    "cte": (re.compile(r"\bWITH\s+[a-z_][a-z0-9_]*\s+AS\s*\(", re.IGNORECASE),),
    "recursive_cte": (re.compile(r"\bWITH\s+RECURSIVE\b", re.IGNORECASE),),
    "lateral_join": (re.compile(r"\bLATERAL\b", re.IGNORECASE),),
    "materialized_view": (re.compile(r"\bCREATE\s+MATERIALIZED\s+VIEW\b", re.IGNORECASE),),
    "view": (re.compile(r"\bCREATE\s+(?:OR\s+REPLACE\s+)?VIEW\b", re.IGNORECASE),),
    "upsert": (re.compile(r"\bON\s+CONFLICT\b", re.IGNORECASE),),
    "jsonb": (re.compile(r"\bjsonb\b|::\s*jsonb", re.IGNORECASE),),
    "array": (re.compile(r"\bARRAY\s*\[|\bunnest\s*\(", re.IGNORECASE),),
}


@dataclass(frozen=True)
class LintIssue:
    kind: str
    path: Path
    message: str
    severity: str = "warning"


@dataclass(frozen=True)
class LintReport:
    files_checked: int
    warnings: tuple[LintIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.warnings


def lint_content(*, path_globs: tuple[str, ...] = ()) -> LintReport:
    files = [
        path
        for path in validate.discover_content_files(path_globs=path_globs)
        if path.name in {"lesson.json", "exercise.json"}
    ]
    warnings: list[LintIssue] = []

    for content_path in files:
        kind = validate.infer_kind(content_path)
        if kind == "exercise":
            warnings.extend(_exercise_warnings(content_path))
            continue
        if kind != "lesson":
            continue
        try:
            lesson = validate.load_content_file(content_path)
        except (OSError, ValueError) as exc:
            warnings.append(LintIssue("lesson", content_path, f"could not load lesson: {exc}"))
            continue

        body_path_value = lesson.get("body_path")
        if not isinstance(body_path_value, str):
            continue
        body_path = content_path.parent / body_path_value
        if not body_path.is_file():
            warnings.append(
                LintIssue("lesson", content_path, f"body_path {body_path_value!r} missing")
            )
            continue

        body = body_path.read_text(encoding="utf-8")
        warnings.extend(_body_warnings(body_path, body, active=lesson.get("status") == "active"))

    return LintReport(files_checked=len(files), warnings=tuple(warnings))


def _exercise_warnings(exercise_path: Path) -> list[LintIssue]:
    warnings: list[LintIssue] = []
    try:
        exercise = validate.load_content_file(exercise_path)
    except (OSError, ValueError) as exc:
        return [LintIssue("exercise", exercise_path, f"could not load exercise: {exc}")]

    solution_path = exercise_path.parent / "solution.sql"
    if not solution_path.is_file():
        return warnings

    solution_sql = solution_path.read_text(encoding="utf-8")
    for concept in exercise.get("not_yet_allowed_concepts", []):
        if not isinstance(concept, str):
            continue
        for pattern in FORBIDDEN_SQL_PATTERNS.get(concept, ()):
            if pattern.search(solution_sql):
                warnings.append(
                    LintIssue(
                        "exercise",
                        solution_path,
                        f"solution.sql appears to use not-yet-allowed concept {concept!r}",
                    )
                )
                break
    return warnings


def _body_warnings(body_path: Path, body: str, *, active: bool) -> list[LintIssue]:
    warnings: list[LintIssue] = []

    if active and len(WORD_RE.findall(body)) < 400:
        warnings.append(
            LintIssue("lesson", body_path, "active lesson body must be at least 400 words")
        )

    for title in SECTION_TITLES:
        pattern = re.compile(rf"^#+\s+{re.escape(title)}\s*$", re.MULTILINE | re.IGNORECASE)
        if not pattern.search(body):
            warnings.append(LintIssue("lesson", body_path, f"missing section: {title}"))

    for match in BARE_URL_RE.finditer(body):
        warnings.append(
            LintIssue("lesson", body_path, f"bare URL lacks markdown title: {match.group(0)}")
        )

    if active and TODO_RE.search(body):
        warnings.append(LintIssue("lesson", body_path, "active body contains TODO/TBD/XXX token"))

    return warnings

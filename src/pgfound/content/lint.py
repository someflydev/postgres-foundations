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
        if path.name == "lesson.json"
    ]
    warnings: list[LintIssue] = []

    for lesson_path in files:
        try:
            lesson = validate.load_content_file(lesson_path)
        except (OSError, ValueError) as exc:
            warnings.append(LintIssue("lesson", lesson_path, f"could not load lesson: {exc}"))
            continue

        body_path_value = lesson.get("body_path")
        if not isinstance(body_path_value, str):
            continue
        body_path = lesson_path.parent / body_path_value
        if not body_path.is_file():
            warnings.append(
                LintIssue("lesson", lesson_path, f"body_path {body_path_value!r} missing")
            )
            continue

        body = body_path.read_text(encoding="utf-8")
        warnings.extend(_body_warnings(body_path, body, active=lesson.get("status") == "active"))

    return LintReport(files_checked=len(files), warnings=tuple(warnings))


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

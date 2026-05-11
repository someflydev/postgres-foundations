"""Schema review helpers."""

from __future__ import annotations

import re
from pathlib import Path

from pgfound.review.models import Finding, Signal

CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
CONSTRAINT_RE = re.compile(r"\b(PRIMARY\s+KEY|FOREIGN\s+KEY|CHECK|UNIQUE|EXCLUDE)\b", re.IGNORECASE)


def lint_schema(path: Path) -> tuple[list[Signal], list[Finding]]:
    """Emit coarse schema-literacy signals from a SQL artifact."""
    if not path.is_file():
        return (
            [Signal("schema_files_present", "missing", f"Missing schema file: {path}", str(path))],
            [
                Finding(
                    "error",
                    "Schema file missing",
                    f"Expected schema artifact at {path}",
                    str(path),
                    "Schema Design: Reviewability",
                )
            ],
        )
    text = path.read_text(encoding="utf-8")
    signals = [
        Signal("schema_files_present", "present", "Schema file is present.", str(path)),
        Signal(
            "expected_tables_present",
            "present" if CREATE_TABLE_RE.search(text) else "missing",
            "Checked for CREATE TABLE statements.",
            str(path),
        ),
        Signal(
            "constraints_present",
            "present" if CONSTRAINT_RE.search(text) else "missing",
            "Checked for primary, foreign, unique, check, or exclusion constraints.",
            str(path),
        ),
    ]
    findings: list[Finding] = []
    if signals[1].value == "missing":
        findings.append(
            Finding(
                "error",
                "No CREATE TABLE statements found",
                "The schema artifact does not appear to create durable tables.",
                str(path),
                "Schema Design: Business truth",
            )
        )
    if signals[2].value == "missing":
        findings.append(
            Finding(
                "warning",
                "No explicit constraints found",
                "The schema needs review for keys and invariant protection.",
                str(path),
                "Schema Design: Constraints",
            )
        )
    return signals, findings

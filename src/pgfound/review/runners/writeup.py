"""Writeup lint runner."""

from __future__ import annotations

import re
from pathlib import Path

from pgfound.review.models import Finding, Signal

WORD_RE = re.compile(r"[A-Za-z0-9_']+")


def lint_writeup(
    path: Path,
    *,
    required_sections: list[str],
    minimum_words_per_section: int = 40,
) -> tuple[list[Signal], list[Finding]]:
    """Check required sections, section word counts, and extension posture text."""
    if not path.is_file():
        return (
            [Signal("writeup_required_sections", "missing", f"Missing writeup: {path}", str(path))],
            [
                Finding(
                    "error",
                    "Writeup missing",
                    f"Expected writeup artifact at {path}",
                    str(path),
                    "Writeup and defense",
                )
            ],
        )

    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    signals: list[Signal] = []
    findings: list[Finding] = []
    missing = [section for section in required_sections if section.lower() not in lower]
    if missing:
        signals.append(
            Signal("writeup_required_sections", "missing", ", ".join(missing), str(path))
        )
        findings.append(
            Finding(
                "warning",
                "Writeup is missing required sections",
                ", ".join(missing),
                str(path),
                "Writeup and defense",
            )
        )
    else:
        signals.append(
            Signal(
                "writeup_required_sections",
                "present",
                "All required section labels were found.",
                str(path),
            )
        )

    sparse = _sparse_sections(text, required_sections, minimum_words_per_section)
    if sparse:
        signals.append(
            Signal("writeup_minimum_word_count", "missing", ", ".join(sparse), str(path))
        )
        findings.append(
            Finding(
                "warning",
                "Writeup sections need more evidence",
                ", ".join(sparse),
                str(path),
                "Writeup and defense",
            )
        )
    else:
        signals.append(
            Signal(
                "writeup_minimum_word_count",
                "present",
                "Required sections meet the minimum word threshold.",
                str(path),
            )
        )

    has_posture = "extension posture" in lower or "not yet" in lower
    signals.append(
        Signal(
            "extension_posture_not_yet",
            "present" if has_posture else "missing",
            "Checked for extension posture or not-yet language.",
            str(path),
        )
    )
    if not has_posture:
        findings.append(
            Finding(
                "warning",
                "Extension posture block missing",
                "Add an explicit not-yet/extension posture section.",
                str(path),
                "Extension Posture: Now versus later",
            )
        )
    return signals, findings


def _sparse_sections(text: str, required_sections: list[str], minimum_words: int) -> list[str]:
    if not required_sections:
        return []
    lower = text.lower()
    starts = sorted(
        (lower.find(section.lower()), section)
        for section in required_sections
        if lower.find(section.lower()) >= 0
    )
    sparse: list[str] = []
    for index, (start, section) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(text)
        body = text[start:end]
        if len(WORD_RE.findall(body)) < minimum_words:
            sparse.append(section)
    return sparse

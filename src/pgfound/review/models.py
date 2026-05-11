"""Shared review engine data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

ReviewMode = Literal["auto", "writeup", "full"]


@dataclass(frozen=True)
class EvaluationContext:
    """Runtime context for a review invocation."""

    repo_root: Path
    db_url: str | None = None


@dataclass(frozen=True)
class EvaluationRequest:
    """Input to the review engine."""

    target_id: str
    artifact_path: Path
    context: EvaluationContext
    mode: ReviewMode = "auto"
    target_kind: Literal["exercise", "capstone"] = "exercise"


@dataclass(frozen=True)
class Signal:
    """Machine-observed evidence consumed by rubric scoring."""

    key: str
    value: str
    detail: str = ""
    pointer: str | None = None


@dataclass(frozen=True)
class Finding:
    """Human-readable review finding."""

    severity: Literal["info", "warning", "error"]
    title: str
    detail: str
    pointer: str | None = None
    dimension: str | None = None


@dataclass(frozen=True)
class DimensionScore:
    """Scored rubric dimension."""

    name: str
    score: int
    max_score: int
    weight: float
    contribution: float
    manual_review: bool = False
    evidence: tuple[Signal, ...] = ()


@dataclass(frozen=True)
class EvaluationResult:
    """Structured review engine output."""

    target_id: str
    target_kind: str
    rubric_id: str
    dimensions: tuple[DimensionScore, ...]
    overall_score: float
    passed: bool
    findings: tuple[Finding, ...] = ()
    signals: tuple[Signal, ...] = ()
    plan_diffs: tuple[dict[str, Any], ...] = ()
    report_paths: dict[str, str] = field(default_factory=dict)

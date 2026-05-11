"""Machine-readable review report writer."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from pgfound.review.models import EvaluationResult


def result_to_dict(result: EvaluationResult) -> dict[str, object]:
    """Convert an evaluation result to the stable report schema."""
    return {
        "target_id": result.target_id,
        "exercise_id": result.target_id if result.target_kind == "exercise" else None,
        "capstone_id": result.target_id if result.target_kind == "capstone" else None,
        "target_kind": result.target_kind,
        "rubric_id": result.rubric_id,
        "overall_score": result.overall_score,
        "pass": result.passed,
        "dimensions": [asdict(dimension) for dimension in result.dimensions],
        "findings": [asdict(finding) for finding in result.findings],
        "signals": [asdict(signal) for signal in result.signals],
        "plan_diffs": list(result.plan_diffs),
    }


def write_json(result: EvaluationResult, path: Path) -> Path:
    """Write a JSON report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result_to_dict(result), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path

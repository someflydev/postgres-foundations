"""Prompt 43 scoring model placeholder."""

from __future__ import annotations

from typing import Any

SCORE_KEYS = (
    "domain_fit",
    "data_shape_fit",
    "workload_fit",
    "operational_feasibility",
    "growth_urgency",
    "portability_penalty",
    "complexity_penalty",
)


def empty_score_breakdown() -> dict[str, float]:
    """Return the report score shape before Prompt 43 lands weighted scoring."""
    return {key: 0.0 for key in SCORE_KEYS}


def average_scoring(actions: list[dict[str, Any]]) -> dict[str, float]:
    """Average rule scoring hints into the report shape.

    This is intentionally simple. Prompt 43 replaces it with the full scoring
    model while preserving the current report contract.
    """
    totals = empty_score_breakdown()
    counts = {key: 0 for key in SCORE_KEYS}
    for action in actions:
        scoring = action.get("scoring", {})
        for key in SCORE_KEYS:
            if key in scoring:
                totals[key] += float(scoring[key])
                counts[key] += 1
    return {
        key: round(totals[key] / counts[key], 3) if counts[key] else 0.0
        for key in SCORE_KEYS
    }

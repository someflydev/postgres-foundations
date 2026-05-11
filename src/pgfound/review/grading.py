"""Rubric signal scoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.review.models import DimensionScore, Signal


def load_rubric(rubric_id: str) -> dict[str, Any]:
    """Load a rubric by ID from default rubrics or capstone-local rubrics."""
    for rubric_path in _rubric_paths():
        data = json.loads(rubric_path.read_text(encoding="utf-8"))
        if data.get("id") == rubric_id:
            return data
    msg = f"rubric {rubric_id!r} not found"
    raise ValueError(msg)


def expanded_dimensions(rubric: dict[str, Any]) -> list[dict[str, Any]]:
    """Return dimensions with composition weights applied."""
    dimensions: list[dict[str, Any]] = []
    for dimension in rubric.get("dimensions", []):
        if isinstance(dimension, dict):
            dimensions.append(dict(dimension))

    for extension in rubric.get("extends", []):
        if not isinstance(extension, dict):
            continue
        base = load_rubric(str(extension["rubric_id"]))
        extension_weight = float(extension["weight"])
        for dimension in expanded_dimensions(base):
            weighted = dict(dimension)
            weighted["name"] = f"{base['title']}: {dimension['name']}"
            weighted["weight"] = float(dimension.get("weight", 0)) * extension_weight
            dimensions.append(weighted)

    for dimension in rubric.get("own_dimensions", []):
        if isinstance(dimension, dict):
            dimensions.append(dict(dimension))
    return dimensions


def evaluate_rubric(
    rubric: dict[str, Any],
    signals: list[Signal],
) -> tuple[tuple[DimensionScore, ...], float, bool]:
    """Score rubric dimensions from observed signals.

    Dimensions with no matching observed signal stay at -1 and are excluded from
    the normalized automatic score while being flagged for manual review.
    """
    signal_by_key = {signal.key: signal for signal in signals}
    dimensions: list[DimensionScore] = []
    scored_weight = 0.0
    weighted_score = 0.0

    for dimension in expanded_dimensions(rubric):
        score: int | None = None
        evidence: list[Signal] = []
        for mapping in dimension.get("signals", []):
            if not isinstance(mapping, dict):
                continue
            key = str(mapping.get("pattern", ""))
            signal = signal_by_key.get(key)
            if signal is None:
                continue
            levels = mapping.get("levels", {})
            if isinstance(levels, dict) and signal.value in levels:
                observed = int(levels[signal.value])
                score = observed if score is None else min(score, observed)
                evidence.append(signal)

        weight = float(dimension.get("weight", 0))
        if score is None:
            dimensions.append(
                DimensionScore(
                    name=str(dimension["name"]),
                    score=-1,
                    max_score=4,
                    weight=weight,
                    contribution=0.0,
                    manual_review=True,
                )
            )
            continue

        contribution = weight * (score / 4)
        scored_weight += weight
        weighted_score += contribution
        dimensions.append(
            DimensionScore(
                name=str(dimension["name"]),
                score=score,
                max_score=4,
                weight=weight,
                contribution=contribution,
                evidence=tuple(evidence),
            )
        )

    overall = weighted_score / scored_weight if scored_weight else 0.0
    passed = overall >= float(rubric.get("pass_threshold", 1.0))
    return tuple(dimensions), overall, passed


def _rubric_paths() -> list[Path]:
    return sorted(paths.RUBRICS_DIR.glob("**/*.json")) + sorted(
        paths.CAPSTONES_DIR.glob("*/rubric.json")
    )

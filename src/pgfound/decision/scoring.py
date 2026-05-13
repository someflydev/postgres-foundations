"""Decision recommendation scoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pgfound import paths

SCORE_KEYS = (
    "domain_fit",
    "data_shape_fit",
    "workload_fit",
    "operational_feasibility",
    "growth_urgency",
    "portability_penalty",
    "complexity_penalty",
)
DEFAULT_WEIGHTS = {
    "domain_fit": 0.2,
    "data_shape_fit": 0.2,
    "workload_fit": 0.2,
    "operational_feasibility": 0.15,
    "growth_urgency": 0.1,
    "portability_penalty": -0.1,
    "complexity_penalty": -0.05,
}
WEIGHTS_PATH = paths.DECISION_ENGINE_DIR / "scoring-weights.json"


def clamp(value: float) -> float:
    """Clamp a numeric score to the report range."""
    return max(0.0, min(1.0, value))


def empty_score_breakdown() -> dict[str, float]:
    """Return the per-dimension score shape."""
    return {key: 0.0 for key in SCORE_KEYS}


def load_weights(path: Path = WEIGHTS_PATH) -> dict[str, float]:
    """Load scoring weights, falling back to the documented defaults."""
    if not path.is_file():
        return dict(DEFAULT_WEIGHTS)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    weights = dict(DEFAULT_WEIGHTS)
    weights.update({key: float(value) for key, value in loaded.items() if key in SCORE_KEYS})
    return weights


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def _operational_cost_level(catalog_entry: dict[str, Any] | None) -> str:
    if not catalog_entry or "operational_cost" not in catalog_entry:
        return "none"
    text = str((catalog_entry or {}).get("operational_cost", "")).lower()
    if "high" in text or "significant" in text:
        return "high"
    if "medium" in text:
        return "medium"
    if "low" in text:
        return "low"
    return "medium"


def _operational_cost_penalty(level: str) -> float:
    return {"none": 0.0, "low": 0.12, "medium": 0.35, "high": 0.72}.get(level, 0.35)


def _team_capacity(intake: dict[str, Any]) -> float:
    team_size = int(intake.get("organization", {}).get("team_size_engineers") or 0)
    tolerance = intake.get("organization", {}).get("operational_tolerance", "medium")
    base = 0.35 if team_size <= 3 else 0.55 if team_size <= 8 else 0.72 if team_size <= 20 else 0.86
    tolerance_adjustment = {"low": -0.12, "medium": 0.0, "high": 0.1}.get(tolerance, 0.0)
    return clamp(base + tolerance_adjustment)


def _portability_penalty(intake: dict[str, Any], catalog_entry: dict[str, Any] | None) -> float:
    organization = intake.get("organization", {})
    constraints = set(organization.get("portability_constraints", []))
    managed_requirement = organization.get("managed_service_requirement")
    availability = (catalog_entry or {}).get("managed_service_availability", "broadly_available")
    if not constraints and managed_requirement != "mandatory":
        return 0.0
    if availability == "broadly_available":
        return 0.04 if constraints else 0.02
    if availability == "limited":
        return 0.24 if managed_requirement == "mandatory" else 0.16
    return 0.45


def _growth_urgency(intake: dict[str, Any], baseline: float) -> float:
    scale = intake.get("scale_signals", {})
    largest_rows = max(scale.get("row_counts_largest_tables", {}).values(), default=0)
    write_rate = float(scale.get("write_throughput_rows_per_sec") or 0)
    read_rate = float(scale.get("read_throughput_qps") or 0)
    connections = float(scale.get("concurrent_connections_peak") or 0)
    growth = float(scale.get("growth_rate_month_over_month") or 0)
    signals = [
        largest_rows >= 10_000_000,
        write_rate >= 100,
        read_rate >= 1000,
        connections >= 150,
        growth >= 0.08,
    ]
    pressure = sum(1 for signal in signals if signal) / len(signals)
    return clamp((baseline * 0.55) + (pressure * 0.45))


def score_action(
    action: dict[str, Any],
    intake: dict[str, Any],
    catalog_entry: dict[str, Any] | None,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Score one recommendation action against intake and catalog context."""
    weights = weights or load_weights()
    baseline = empty_score_breakdown()
    baseline.update({key: clamp(float(value)) for key, value in action.get("scoring", {}).items()})

    cost_level = _operational_cost_level(catalog_entry)
    cost_penalty = _operational_cost_penalty(cost_level)
    capacity = _team_capacity(intake)

    score_breakdown = dict(baseline)
    if not action.get("scoring"):
        confidence = float(action.get("confidence", 0.5))
        score_breakdown.update(
            {
                "domain_fit": confidence,
                "data_shape_fit": confidence,
                "workload_fit": confidence,
                "operational_feasibility": capacity,
                "growth_urgency": 0.35,
                "portability_penalty": 0.0,
                "complexity_penalty": cost_penalty,
            }
        )

    score_breakdown["operational_feasibility"] = clamp(
        (score_breakdown["operational_feasibility"] * 0.65)
        + (capacity * 0.35)
        - (cost_penalty * 0.12)
    )
    score_breakdown["growth_urgency"] = _growth_urgency(intake, score_breakdown["growth_urgency"])
    score_breakdown["portability_penalty"] = clamp(
        max(score_breakdown["portability_penalty"], _portability_penalty(intake, catalog_entry))
    )
    score_breakdown["complexity_penalty"] = clamp(
        max(score_breakdown["complexity_penalty"], cost_penalty)
    )
    if action.get("target_slug") == "row_level_security" and "rls_required" in intake.get(
        "security_constraints", []
    ):
        score_breakdown["domain_fit"] = clamp(score_breakdown["domain_fit"] + 0.06)
        score_breakdown["data_shape_fit"] = clamp(score_breakdown["data_shape_fit"] + 0.06)
        score_breakdown["workload_fit"] = clamp(score_breakdown["workload_fit"] + 0.06)

    operational_cost = str((catalog_entry or {}).get("operational_cost", ""))
    if _contains_any(operational_cost, ("high", "significant")):
        score_breakdown["operational_feasibility"] = clamp(
            score_breakdown["operational_feasibility"] - 0.08
        )

    total = sum(score_breakdown[key] * weights[key] for key in SCORE_KEYS)
    return {
        "score_breakdown": {key: round(clamp(score_breakdown[key]), 3) for key in SCORE_KEYS},
        "recommendation_score": round(clamp(total), 3),
    }


def average_breakdowns(items: list[dict[str, Any]]) -> dict[str, float]:
    """Average per-recommendation score breakdowns for report rollups."""
    if not items:
        return empty_score_breakdown()
    totals = empty_score_breakdown()
    for item in items:
        breakdown = item.get("score_breakdown", {})
        for key in SCORE_KEYS:
            totals[key] += float(breakdown.get(key, 0.0))
    return {key: round(totals[key] / len(items), 3) for key in SCORE_KEYS}

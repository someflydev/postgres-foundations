"""Decision scenario helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pgfound import paths
from pgfound.decision import engine

RECOMMENDATION_CLASSES = (
    "recommend_now",
    "candidate_later",
    "not_enough_evidence",
    "avoid_for_now",
)


@dataclass(frozen=True)
class ExtensionCoverageRow:
    """Coverage counts for one extension across industry scenarios."""

    extension_slug: str
    recommend_now: int
    candidate_later: int
    not_enough_evidence: int
    avoid_for_now: int


def industry_scenario_intakes(root: Path | None = None) -> list[Path]:
    """Return authored industry scenario intake paths."""
    scenario_root = root or paths.SCENARIOS_DIR / "industries"
    return sorted(scenario_root.glob("*/*/intake.json"))


def extension_coverage(root: Path | None = None) -> list[ExtensionCoverageRow]:
    """Count extension recommendation classes across industry scenarios."""
    counts: dict[str, dict[str, int]] = {
        entry["id"]: {recommendation_class: 0 for recommendation_class in RECOMMENDATION_CLASSES}
        for entry in engine.load_catalog("extension")
    }

    for intake_path in industry_scenario_intakes(root):
        report = engine.run_decision(intake_path)
        seen_in_scenario: set[tuple[str, str]] = set()
        for recommendation in report["recommendations"]:
            if recommendation["kind"] != "extension":
                continue
            target_slug = recommendation["target_slug"]
            recommendation_class = recommendation["recommendation_class"]
            key = (target_slug, recommendation_class)
            if target_slug not in counts or recommendation_class not in RECOMMENDATION_CLASSES:
                continue
            if key in seen_in_scenario:
                continue
            counts[target_slug][recommendation_class] += 1
            seen_in_scenario.add(key)

    return [
        ExtensionCoverageRow(
            extension_slug=extension_slug,
            recommend_now=class_counts["recommend_now"],
            candidate_later=class_counts["candidate_later"],
            not_enough_evidence=class_counts["not_enough_evidence"],
            avoid_for_now=class_counts["avoid_for_now"],
        )
        for extension_slug, class_counts in sorted(counts.items())
    ]

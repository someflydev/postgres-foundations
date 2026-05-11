"""Concurrency review runner wrapper."""

from __future__ import annotations

from pathlib import Path

from pgfound.lab import harness
from pgfound.review.models import Finding, Signal


def run_scenario(path: Path) -> tuple[list[Signal], list[Finding]]:
    """Run a concurrency scenario and convert its result to signals."""
    report = harness.run_scenario_path(path)
    if report.ok:
        return (
            [Signal("concurrency_scenario_passes", "present", f"{path.name} passed.", str(path))],
            [
                Finding(
                    "info",
                    "Concurrency scenario passed",
                    f"{path.name} matched its expected transcript.",
                    str(path),
                    "Concurrency",
                )
            ],
        )
    return (
        [
            Signal(
                "concurrency_scenario_passes",
                "missing",
                report.diff or "Scenario failed.",
                str(path),
            )
        ],
        [
            Finding(
                "error",
                "Concurrency scenario failed",
                report.diff or "Scenario failed.",
                str(path),
                "Concurrency",
            )
        ],
    )

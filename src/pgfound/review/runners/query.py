"""Query review runner and plan diff helpers."""

from __future__ import annotations

from typing import Any

from pgfound.lab import explain
from pgfound.review.models import Finding, Signal


def compare_correctness(
    correct: bool, diff: str, *, pointer: str | None = None
) -> tuple[list[Signal], list[Finding]]:
    """Convert an exercise comparator result to review signals and findings."""
    if correct:
        return (
            [
                Signal(
                    "output_matches_reference",
                    "present",
                    "Answer matches reference output.",
                    pointer,
                )
            ],
            [
                Finding(
                    "info",
                    "Output matches reference",
                    "The answer returned the reference row set.",
                    pointer,
                )
            ],
        )
    detail = diff or "The answer did not match the reference output."
    return (
        [Signal("output_matches_reference", "missing", detail, pointer)],
        [Finding("error", "Output differs from reference", detail, pointer, "Result semantics")],
    )


def diff_plans(reference: dict[str, Any], learner: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic, compact plan comparison."""
    left = explain.summarize_plan(reference)
    right = explain.summarize_plan(learner)
    return {
        "node_count_delta": right.node_count - left.node_count,
        "total_cost_delta": round(right.total_cost - left.total_cost, 3),
        "execution_time_ms_delta": round(right.actual_time - left.actual_time, 3),
        "estimated_rows_delta": right.plan_rows - left.plan_rows,
        "actual_rows_delta": right.actual_rows - left.actual_rows,
        "shared_hit_blocks_delta": right.shared_hit_blocks - left.shared_hit_blocks,
        "shared_read_blocks_delta": right.shared_read_blocks - left.shared_read_blocks,
        "reference_node_types": list(left.node_types),
        "learner_node_types": list(right.node_types),
    }


def plan_signals(
    plan_diff: dict[str, Any], *, pointer: str | None = None
) -> tuple[list[Signal], list[Finding]]:
    """Emit basic index/estimate signals from a plan diff."""
    signals: list[Signal] = []
    findings: list[Finding] = []
    learner_nodes = set(plan_diff.get("learner_node_types", []))
    reference_nodes = set(plan_diff.get("reference_node_types", []))

    if "Seq Scan" in learner_nodes and "Seq Scan" not in reference_nodes:
        signals.append(
            Signal(
                "seq_scan_where_index_expected",
                "present",
                "Learner plan uses a Seq Scan where the reference does not.",
                pointer,
            )
        )
        findings.append(
            Finding(
                "warning",
                "Sequential scan where index access was expected",
                "Review the predicate and available index for the hot query.",
                pointer,
                "Plan evidence",
            )
        )
    else:
        signals.append(
            Signal(
                "seq_scan_where_index_expected",
                "absent",
                "No unexpected Seq Scan detected.",
                pointer,
            )
        )

    if any("Index" in node for node in reference_nodes) and not any(
        "Index" in node for node in learner_nodes
    ):
        signals.append(
            Signal(
                "btree_not_used",
                "present",
                "Reference uses index access but learner plan does not.",
                pointer,
            )
        )
    else:
        signals.append(
            Signal(
                "btree_not_used",
                "absent",
                "Index access posture matches the reference closely enough.",
                pointer,
            )
        )

    estimated_delta = abs(int(plan_diff.get("estimated_rows_delta", 0)))
    actual_delta = abs(int(plan_diff.get("actual_rows_delta", 0)))
    value = "present" if actual_delta and estimated_delta > max(100, actual_delta * 4) else "absent"
    signals.append(
        Signal(
            "actual_rows_far_from_estimate",
            value,
            "Compared estimated and actual row deltas.",
            pointer,
        )
    )
    return signals, findings

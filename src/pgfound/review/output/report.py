"""Markdown and Rich review report rendering."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from rich.console import Console
from rich.table import Table

from pgfound.review.models import EvaluationResult


def render_console(console: Console, result: EvaluationResult) -> None:
    """Render a concise review summary to the terminal."""
    table = Table(title=f"review: {result.target_id}")
    table.add_column("Dimension")
    table.add_column("Score", justify="right")
    table.add_column("Weight", justify="right")
    table.add_column("Contribution", justify="right")
    for dimension in result.dimensions:
        score = "manual" if dimension.manual_review else f"{dimension.score}/{dimension.max_score}"
        table.add_row(
            dimension.name, score, f"{dimension.weight:.2f}", f"{dimension.contribution:.3f}"
        )
    console.print(table)
    console.print(f"overall={result.overall_score:.3f} pass={result.passed}")
    for finding in result.findings:
        console.print(f"{finding.severity.upper()}: {finding.title} ({finding.pointer or '-'})")


def write_markdown(result: EvaluationResult, path: Path) -> Path:
    """Write a Markdown review report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Review: {result.target_id}",
        "",
        f"- Target kind: `{result.target_kind}`",
        f"- Rubric: `{result.rubric_id}`",
        f"- Overall score: `{result.overall_score:.3f}`",
        f"- Pass: `{str(result.passed).lower()}`",
        "",
        "## Summary",
        "",
        "| Dimension | Score | Weight | Contribution |",
        "| --- | ---: | ---: | ---: |",
    ]
    for dimension in result.dimensions:
        score = (
            "manual review"
            if dimension.manual_review
            else f"{dimension.score}/{dimension.max_score}"
        )
        lines.append(
            f"| {dimension.name} | {score} | {dimension.weight:.3f} | "
            f"{dimension.contribution:.3f} |"
        )

    manual = [dimension for dimension in result.dimensions if dimension.manual_review]
    lines.extend(["", "## Manual-Review Queue", ""])
    if manual:
        for dimension in manual:
            lines.append(
                f"- **{dimension.name}**: inspect learner artifacts and rubric descriptors."
            )
    else:
        lines.append("No manual-review dimensions remain.")

    grouped = defaultdict(list)
    for finding in result.findings:
        grouped[finding.severity].append(finding)
    lines.extend(["", "## Findings", ""])
    if not result.findings:
        lines.append("No findings.")
    for severity in ("error", "warning", "info"):
        if not grouped[severity]:
            continue
        lines.extend([f"### {severity.title()}", ""])
        for finding in grouped[severity]:
            pointer = f" `{finding.pointer}`" if finding.pointer else ""
            dimension = f" [{finding.dimension}]" if finding.dimension else ""
            lines.append(f"- **{finding.title}**{dimension}{pointer}: {finding.detail}")

    if result.plan_diffs:
        lines.extend(["", "## Plan Diffs", ""])
        for diff in result.plan_diffs:
            lines.append("```json")
            import json

            lines.append(json.dumps(diff, indent=2, sort_keys=True))
            lines.append("```")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path

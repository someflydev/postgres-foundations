"""Decision-engine report serialization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

Report = dict[str, Any]


def write_report(report: Report, out_dir: Path) -> tuple[Path, Path]:
    """Write machine-readable JSON and human-readable Markdown reports."""
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "report.json"
    markdown_path = out_dir / "report.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_markdown(report: Report) -> str:
    lines = [
        f"# Decision Report: {report['intake_id']}",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Engine version: `{report['engine_version']}`",
        f"- Recommendations: `{len(report['recommendations'])}`",
        "",
        "## Recommendations",
        "",
    ]
    if report["recommendations"]:
        for recommendation in report["recommendations"]:
            lines.append(f"- `{recommendation['verdict']}` for `{recommendation['target_slug']}`")
    else:
        lines.append("No recommendations yet. Catalogs and rules are authored in later prompts.")
    lines.extend(["", "## Score Breakdown", ""])
    for name, score in report["score_breakdown"].items():
        lines.append(f"- `{name}`: {score:.2f}")
    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- `{warning['anti_pattern_slug']}`: {warning['message']}")
    else:
        lines.append("No warnings.")
    lines.extend(["", "## Followup Questions", ""])
    if report["followup_questions"]:
        for question in report["followup_questions"]:
            lines.append(f"- {question}")
    else:
        lines.append("No followup questions yet.")
    return "\n".join(lines) + "\n"

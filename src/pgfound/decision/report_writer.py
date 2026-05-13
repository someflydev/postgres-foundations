"""Decision-engine report serialization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

Report = dict[str, Any]
TEMPLATE_DIR = Path(__file__).parent / "templates"


def _environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=False,
        lstrip_blocks=True,
    )
    env.filters["score"] = lambda value: f"{float(value):.2f}"
    return env


def write_report(report: Report, out_dir: Path, show_scores: bool = True) -> tuple[Path, Path]:
    """Write machine-readable JSON and human-readable Markdown reports."""
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "report.json"
    markdown_path = out_dir / "report.md"
    json_path.write_text(render_json(report), encoding="utf-8")
    markdown_path.write_text(render_markdown(report, show_scores=show_scores), encoding="utf-8")
    return json_path, markdown_path


def render_json(report: Report) -> str:
    """Render report JSON exactly as the CLI should emit it."""
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def render_markdown(report: Report, show_scores: bool = True) -> str:
    """Render the architect-facing Markdown report."""
    template = _environment().get_template("decision_report.md.j2")
    return template.render(report=report, show_scores=show_scores)

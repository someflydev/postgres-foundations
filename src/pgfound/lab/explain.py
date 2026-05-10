"""EXPLAIN helpers for the PostgreSQL lab."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from pgfound import paths
from pgfound.content.seed import database_url

PLAN_DIR = paths.TMP_DIR / "plans"


@dataclass(frozen=True)
class PlanSummary:
    node_count: int
    total_cost: float
    actual_time: float
    plan_rows: int
    actual_rows: int
    shared_hit_blocks: int
    shared_read_blocks: int
    node_types: tuple[str, ...]


def read_sql(value: str | None) -> str | None:
    """Read SQL from a path when it exists, otherwise treat the value as inline SQL."""
    if value is None:
        return None
    candidate = Path(value)
    if candidate.is_file():
        return candidate.read_text(encoding="utf-8")
    return value


def explain_sql(sql: str) -> dict[str, Any]:
    """Run EXPLAIN JSON against the configured lab database."""
    explain = "EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON) " + sql.rstrip().rstrip(";")
    with psycopg.connect(database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(explain)
            raw_plan = cursor.fetchone()
    if raw_plan is None:
        msg = "EXPLAIN returned no rows"
        raise RuntimeError(msg)
    plan_value = raw_plan[0]
    if isinstance(plan_value, str):
        plan_value = json.loads(plan_value)
    if not isinstance(plan_value, list) or not plan_value:
        msg = "EXPLAIN returned an unexpected JSON shape"
        raise RuntimeError(msg)
    return plan_value[0]


def save_plan(label: str, plan: dict[str, Any]) -> Path:
    """Persist a JSON plan under tmp/plans."""
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    path = plan_path(label)
    path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_plan(label: str) -> dict[str, Any]:
    """Load a saved plan by label."""
    candidate = Path(label)
    path = candidate if candidate.is_file() else plan_path(label)
    if not path.is_file():
        relative = path.relative_to(paths.REPO_ROOT)
        msg = f"plan baseline not found: {relative}"
        raise FileNotFoundError(msg)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        msg = f"plan baseline has unexpected shape: {label}"
        raise ValueError(msg)
    return loaded


def plan_path(label: str) -> Path:
    """Return the path for a baseline label."""
    safe = label.replace("/", "_")
    return PLAN_DIR / f"{safe}.json"


def render_plan(console: Console, plan: dict[str, Any], *, sql: str | None = None) -> None:
    """Print SQL and a simplified plan tree."""
    if sql:
        console.print(Panel(Syntax(sql.rstrip(), "sql", word_wrap=True), title="SQL"))
    root = plan.get("Plan")
    tree = Tree(_node_label(root if isinstance(root, dict) else {}), guide_style="dim")
    if isinstance(root, dict):
        _add_children(tree, root)
    console.print(tree)

    summary = summarize_plan(plan)
    table = Table(title="Plan summary")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("nodes", str(summary.node_count))
    table.add_row("total cost", f"{summary.total_cost:.2f}")
    table.add_row("execution time ms", f"{summary.actual_time:.3f}")
    table.add_row("estimated rows", str(summary.plan_rows))
    table.add_row("actual rows", str(summary.actual_rows))
    table.add_row("shared hit blocks", str(summary.shared_hit_blocks))
    table.add_row("shared read blocks", str(summary.shared_read_blocks))
    console.print(table)


def render_diff(console: Console, before: dict[str, Any], after: dict[str, Any]) -> None:
    """Print a compact diff between two plan summaries."""
    left = summarize_plan(before)
    right = summarize_plan(after)
    table = Table(title="Plan comparison")
    table.add_column("Metric")
    table.add_column("Before", justify="right")
    table.add_column("After", justify="right")
    table.add_column("Delta", justify="right")
    rows = [
        ("nodes", left.node_count, right.node_count),
        ("total cost", left.total_cost, right.total_cost),
        ("execution time ms", left.actual_time, right.actual_time),
        ("estimated rows", left.plan_rows, right.plan_rows),
        ("actual rows", left.actual_rows, right.actual_rows),
        ("shared hit blocks", left.shared_hit_blocks, right.shared_hit_blocks),
        ("shared read blocks", left.shared_read_blocks, right.shared_read_blocks),
    ]
    for label, before_value, after_value in rows:
        delta = after_value - before_value
        if isinstance(before_value, float) or isinstance(after_value, float):
            table.add_row(label, f"{before_value:.3f}", f"{after_value:.3f}", f"{delta:+.3f}")
        else:
            table.add_row(label, str(before_value), str(after_value), f"{delta:+d}")
    table.add_row("node types", " -> ".join(left.node_types), " -> ".join(right.node_types), "")
    console.print(table)


def summarize_plan(plan: dict[str, Any]) -> PlanSummary:
    """Reduce PostgreSQL's plan JSON to the metrics learners compare first."""
    nodes = list(_walk_nodes(plan.get("Plan")))
    root = nodes[0] if nodes else {}
    return PlanSummary(
        node_count=len(nodes),
        total_cost=float(root.get("Total Cost", 0)),
        actual_time=float(plan.get("Execution Time", root.get("Actual Total Time", 0))),
        plan_rows=sum(int(node.get("Plan Rows", 0)) for node in nodes),
        actual_rows=sum(int(node.get("Actual Rows", 0)) for node in nodes),
        shared_hit_blocks=sum(int(node.get("Shared Hit Blocks", 0)) for node in nodes),
        shared_read_blocks=sum(int(node.get("Shared Read Blocks", 0)) for node in nodes),
        node_types=tuple(str(node.get("Node Type", "Unknown")) for node in nodes),
    )


def _walk_nodes(node: Any) -> list[dict[str, Any]]:
    if not isinstance(node, dict):
        return []
    nodes = [node]
    for child in node.get("Plans", []):
        nodes.extend(_walk_nodes(child))
    return nodes


def _add_children(tree: Tree, node: dict[str, Any]) -> None:
    for child in node.get("Plans", []):
        if not isinstance(child, dict):
            continue
        branch = tree.add(_node_label(child))
        _add_children(branch, child)


def _node_label(node: dict[str, Any]) -> str:
    relation = node.get("Relation Name")
    index_name = node.get("Index Name")
    parts = [f"[bold cyan]{node.get('Node Type', 'Unknown')}[/]"]
    if relation:
        parts.append(f"on [green]{relation}[/]")
    if index_name:
        parts.append(f"using [magenta]{index_name}[/]")
    parts.append(f"cost={node.get('Startup Cost', 0):.2f}..{node.get('Total Cost', 0):.2f}")
    parts.append(f"rows={node.get('Plan Rows', 0)}")
    parts.append(f"actual={node.get('Actual Total Time', 0):.3f}ms")
    if "Filter" in node:
        parts.append(f"filter=[yellow]{node['Filter']}[/]")
    if "Index Cond" in node:
        parts.append(f"index_cond=[yellow]{node['Index Cond']}[/]")
    return " ".join(parts)

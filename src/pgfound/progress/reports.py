"""Progress dashboard and export rendering."""

from __future__ import annotations

from pathlib import Path
from statistics import mean

from rich.console import Console
from rich.table import Table

from pgfound import paths
from pgfound.progress import derive
from pgfound.progress.store import ProgressSnapshot


def render_dashboard(
    console: Console, snapshot: ProgressSnapshot, module_id: str | None = None
) -> None:
    progress = derive.compute_module_progress(snapshot.exercise_attempts)
    if module_id:
        module = progress.get(module_id)
        if module is None:
            raise ValueError(f"unknown module: {module_id}")
        table = Table(title=f"pgfound progress: {module_id}")
        table.add_column("Field")
        table.add_column("Value")
        table.add_row("status", module.status)
        table.add_row("first touched", module.first_touched_at or "-")
        table.add_row("exit met", module.exit_met_at or "-")
        table.add_row("evidence", "\n".join(module.evidence) if module.evidence else "-")
        console.print(table)
        return

    profile_name = snapshot.profile.name if snapshot.profile else "uninitialized"
    table = Table(title=f"pgfound progress: {profile_name}")
    table.add_column("Module")
    table.add_column("Status")
    table.add_column("Evidence", overflow="fold")
    for module in progress.values():
        table.add_row(module.module_id, module.status, ", ".join(module.evidence[:2]) or "-")
    console.print(table)

    attempts = sorted(
        snapshot.exercise_attempts,
        key=lambda item: item.completed_at or item.started_at,
        reverse=True,
    )[:3]
    recent = Table(title="recent attempts")
    recent.add_column("Exercise")
    recent.add_column("Result")
    recent.add_column("Completed")
    for attempt in attempts:
        recent.add_row(attempt.exercise_id, attempt.check_result, attempt.completed_at or "-")
    if not attempts:
        recent.add_row("-", "-", "-")
    console.print(recent)

    caps = Table(title="capstones and interviews")
    caps.add_column("Area")
    caps.add_column("Attempts", justify="right")
    caps.add_row("capstones", str(len(snapshot.capstone_attempts)))
    caps.add_row("interviews", str(len(snapshot.interview_attempts)))
    console.print(caps)


def render_export(snapshot: ProgressSnapshot, *, output_format: str) -> str:
    progress = derive.compute_module_progress(snapshot.exercise_attempts)
    if output_format == "json":
        import json

        payload = {
            "profile": snapshot.profile.to_dict() if snapshot.profile else None,
            "modules": [module.to_dict() for module in progress.values()],
            "exercise_attempts": len(snapshot.exercise_attempts),
            "capstone_attempts": len(snapshot.capstone_attempts),
            "interview_attempts": len(snapshot.interview_attempts),
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"

    lines = ["# Progress Summary", ""]
    if snapshot.profile:
        lines.extend([f"Learner: {snapshot.profile.name}", ""])
    lines.append("## Modules")
    for module in progress.values():
        lines.append(f"- {module.module_id}: {module.status}")
    lines.extend(
        [
            "",
            "## Attempts",
            f"- Exercises: {len(snapshot.exercise_attempts)}",
            f"- Capstones: {len(snapshot.capstone_attempts)}",
            f"- Interviews: {len(snapshot.interview_attempts)}",
        ]
    )
    return "\n".join(lines) + "\n"


def render_coach_report(snapshot: ProgressSnapshot, profile_path: Path) -> str:
    progress = derive.compute_module_progress(snapshot.exercise_attempts)
    lines = [
        "# Coach Progress Report",
        "",
        f"Profile path: {profile_path}",
        "",
        "## Latest Attempts",
    ]
    recent = sorted(
        snapshot.exercise_attempts,
        key=lambda item: item.completed_at or item.started_at,
        reverse=True,
    )[:10]
    lines.extend(
        f"- {attempt.exercise_id}: {attempt.check_result} ({attempt.completed_at or '-'})"
        for attempt in recent
    )
    if not recent:
        lines.append("- No exercise attempts recorded.")
    lines.extend(["", "## Rubric Trends"])
    score_buckets: dict[str, list[float]] = {}
    for attempt in snapshot.exercise_attempts:
        for name, score in attempt.rubric_scores.items():
            if score >= 0:
                score_buckets.setdefault(name, []).append(float(score))
    for name, scores in sorted(score_buckets.items()):
        lines.append(f"- {name}: average {mean(scores):.2f} over {len(scores)} attempt(s)")
    if not score_buckets:
        lines.append("- No rubric scores recorded in progress files.")
    lines.extend(["", "## Open Modules"])
    lines.extend(
        f"- {module.module_id}: {module.status}"
        for module in progress.values()
        if module.status != "met"
    )
    lines.extend(["", "## Open Remediation Packs"])
    packs = sorted((paths.TMP_DIR / "remediation").glob("*.md"), reverse=True)[:10]
    lines.extend(f"- {pack.relative_to(paths.REPO_ROOT)}" for pack in packs)
    if not packs:
        lines.append("- None found.")
    lines.extend(["", "## Flagged Manual Review Dimensions"])
    manual = []
    for attempt in snapshot.capstone_attempts:
        manual.extend(name for name, score in attempt.rubric_scores.items() if score < 0)
    lines.extend(f"- {name}" for name in sorted(set(manual))[:20])
    if not manual:
        lines.append("- None recorded in progress files.")
    return "\n".join(lines) + "\n"

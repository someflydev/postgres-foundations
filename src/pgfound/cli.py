"""Click command surface for pgfound."""

import shutil
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

import pgfound
from pgfound import paths
from pgfound.content import loader
from pgfound.content import scaffold as content_scaffold
from pgfound.content import validate as content_validator
from pgfound.lab import compose

console = Console()


def _success(message: str) -> None:
    console.print(message)


@click.group(help="PostgreSQL Foundations platform CLI.")
def main() -> None:
    """Run the pgfound CLI."""


@main.command(help="Print the pgfound package version.")
def version() -> None:
    """Print the pgfound package version."""
    click.echo(pgfound.__version__)


def _required_paths() -> list[tuple[str, Path]]:
    return [
        ("repo root", paths.REPO_ROOT),
        ("docker", paths.DOCKER_DIR),
        ("curriculum", paths.CURRICULUM_DIR),
        ("lessons", paths.LESSONS_DIR),
        ("exercises", paths.EXERCISES_DIR),
        ("scenarios", paths.SCENARIOS_DIR),
        ("capstones", paths.CAPSTONES_DIR),
        ("rubrics", paths.RUBRICS_DIR),
        ("seed data", paths.SEED_DATA_DIR),
        ("decision engine", paths.DECISION_ENGINE_DIR),
        ("llm prompts", paths.LLM_PROMPTS_DIR),
    ]


@main.command(help="Check local prerequisites and repository paths.")
def doctor() -> None:
    """Check local prerequisites and repository paths."""
    checks: list[tuple[str, bool, str]] = []

    python_ok = sys.version_info >= (3, 12)
    checks.append(("Python >= 3.12", python_ok, sys.version.split()[0]))

    docker_path = shutil.which("docker")
    docker_ok = docker_path is not None
    docker_detail = docker_path or "docker CLI not found"
    if docker_ok:
        try:
            version_result = subprocess.run(
                ["docker", "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            docker_detail = version_result.stdout.strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            docker_ok = False
            docker_detail = str(exc)
    checks.append(("Docker CLI available", docker_ok, docker_detail))

    for label, path in _required_paths():
        try:
            paths.ensure_exists(path)
            checks.append((f"path: {label}", True, str(path)))
        except FileNotFoundError as exc:
            checks.append((f"path: {label}", False, str(exc)))

    compose_ok = False
    compose_detail = "skipped because docker CLI is unavailable"
    if docker_ok:
        try:
            subprocess.run(
                ["docker", "compose", "config"],
                cwd=paths.DOCKER_DIR,
                check=True,
                capture_output=True,
                text=True,
            )
            compose_ok = True
            compose_detail = "docker compose config parsed"
        except (OSError, subprocess.CalledProcessError) as exc:
            compose_detail = str(exc)
    checks.append(("Docker Compose config", compose_ok, compose_detail))

    table = Table(title="pgfound doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    for label, ok, detail in checks:
        table.add_row(label, "✅" if ok else "❌", detail)
    console.print(table)

    if not all(ok for _, ok, _ in checks):
        raise click.ClickException("doctor found failing checks")


@main.group(help="Manage the PostgreSQL Docker lab.")
def lab() -> None:
    """Manage the PostgreSQL Docker lab."""


@lab.command("up", help="Start the primary PostgreSQL lab.")
@click.option("--foreground", is_flag=True, help="Run docker compose in the foreground.")
def lab_up(foreground: bool) -> None:
    """Start the primary PostgreSQL lab."""
    compose.up(detach=not foreground)


@lab.command("sandbox-up", help="Start the sandbox PostgreSQL lab profile.")
@click.option("--foreground", is_flag=True, help="Run docker compose in the foreground.")
def lab_sandbox_up(foreground: bool) -> None:
    """Start the sandbox PostgreSQL lab profile."""
    compose.up(detach=not foreground, profile="sandbox")


@lab.command("down", help="Stop the PostgreSQL lab.")
@click.option("--volumes", is_flag=True, help="Remove named Docker volumes too.")
def lab_down(volumes: bool) -> None:
    """Stop the PostgreSQL lab."""
    compose.down(volumes=volumes)


@lab.command("nuke", help="Stop the lab and remove lab volumes.")
def lab_nuke() -> None:
    """Stop the lab and remove lab volumes."""
    compose.down(volumes=True)


@lab.command("psql", help="Open an interactive psql session inside the lab container.")
@click.option("--user", default="pgfound", show_default=True, help="PostgreSQL role to connect as.")
@click.option(
    "--db", default="pgfound", show_default=True, help="PostgreSQL database to connect to."
)
def lab_psql(user: str, db: str) -> None:
    """Open an interactive psql session inside the lab container."""
    compose.exec_psql_interactive(user=user, db=db)


@lab.command("logs", help="Show Docker Compose logs for the lab.")
@click.argument("service", required=False)
@click.option("--follow", "-f", is_flag=True, help="Follow log output.")
def lab_logs(service: str | None, follow: bool) -> None:
    """Show Docker Compose logs for the lab."""
    compose.logs(service=service, follow=follow)


@lab.command("status", help="Show Docker Compose service status.")
def lab_status() -> None:
    """Show Docker Compose service status."""
    rows = compose.ps_json()
    table = Table(title="pgfound lab status")
    table.add_column("Name")
    table.add_column("Service")
    table.add_column("State")
    table.add_column("Ports")
    for row in rows:
        table.add_row(
            str(row.get("Name", "")),
            str(row.get("Service", "")),
            str(row.get("State", "")),
            str(row.get("Publishers", row.get("Ports", ""))),
        )
    console.print(table)


@main.group(help="Inspect and validate platform content.")
def content() -> None:
    """Inspect and validate platform content."""


@content.command("list", help="List content files by kind.")
@click.option(
    "--kind",
    type=click.Choice(["lesson", "exercise", "scenario", "capstone", "rubric"]),
    help="Content kind to list.",
)
def content_list(kind: str | None) -> None:
    """List content files by kind."""
    kinds = [kind] if kind else list(loader.CONTENT_DIRS)
    items = [(item_kind, item) for item_kind in kinds for item in loader.list_content(item_kind)]
    if not items:
        _success("no content yet")
        return

    table = Table(title="pgfound content")
    table.add_column("Kind")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Path")
    for item_kind, item in items:
        table.add_row(item_kind, item.id, item.title, str(item.path.relative_to(paths.REPO_ROOT)))
    console.print(table)


@content.command("show", help="Show raw content for a single item.")
@click.argument("kind", type=click.Choice(["lesson", "exercise", "scenario", "capstone", "rubric"]))
@click.argument("content_id")
def content_show(kind: str, content_id: str) -> None:
    """Show raw content for a single item."""
    loaded = loader.load_raw_content(kind, content_id)
    if loaded is None:
        raise click.ClickException(f"{kind} {content_id!r} not found")
    file_path, raw = loaded
    console.print(f"Raw file content from {file_path}; structured loader expands in PROMPT_05.")
    console.print(raw)


@content.command("validate", help="Validate authored content against JSON Schemas.")
@click.option("--strict", is_flag=True, help="Treat validation warnings as errors.")
@click.option(
    "--paths",
    "path_globs",
    multiple=True,
    help="Restrict validation to a file glob. May be provided more than once.",
)
@click.option(
    "--include-examples",
    is_flag=True,
    help="Also validate schema example files under content-schemas/examples/.",
)
def content_validate(path_globs: tuple[str, ...], include_examples: bool, strict: bool) -> None:
    """Validate content files and schema-level cross references."""
    report = content_validator.validate_content(
        path_globs=path_globs,
        include_examples=include_examples,
        strict=strict,
    )

    table = Table(title="pgfound content validate")
    table.add_column("Kind")
    table.add_column("Files", justify="right")
    table.add_column("Errors", justify="right")
    table.add_column("Warnings", justify="right")
    for kind in content_validator.CONTENT_KINDS:
        errors = sum(1 for issue in report.errors if issue.kind == kind)
        warnings = sum(1 for issue in report.warnings if issue.kind == kind)
        table.add_row(kind, str(report.by_kind[kind]), str(errors), str(warnings))
    console.print(table)

    for issue in (*report.errors, *report.warnings):
        relative = issue.path
        try:
            relative = issue.path.relative_to(paths.REPO_ROOT)
        except ValueError:
            pass
        label = "ERROR" if issue.severity == "error" else "WARNING"
        console.print(f"{label}: {issue.kind}: {relative}")
        console.print(f"  {issue.message}")

    warning_count = len(report.warnings)
    if report.ok:
        _success(
            f"PASS: checked {report.files_checked} file(s), 0 error(s), {warning_count} warning(s)"
        )
        return

    raise click.ClickException(
        f"FAIL: checked {report.files_checked} file(s), "
        f"{len(report.errors)} error(s), {warning_count} warning(s)"
    )


@content.group("scaffold", help="Create draft content files from templates.")
def content_scaffold_group() -> None:
    """Create draft content files from templates."""


@content_scaffold_group.command("lesson", help="Scaffold a draft lesson.")
@click.option("--phase", required=True, type=int, help="Numeric phase from curriculum/map.json.")
@click.option("--cluster", required=True, help="Cluster slug inside the phase.")
@click.option("--slug", required=True, help="Lesson slug and ID.")
@click.option("--title", required=True, help="Human-facing lesson title.")
@click.option("--capability-layer", required=True, help="Capability layer slug.")
def content_scaffold_lesson(
    phase: int,
    cluster: str,
    slug: str,
    title: str,
    capability_layer: str,
) -> None:
    """Scaffold a draft lesson and validate the generated files."""
    try:
        lesson_dir = content_scaffold.scaffold_lesson(
            phase=phase,
            cluster=cluster,
            slug=slug,
            title=title,
            capability_layer=capability_layer,
        )
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    lesson_json = lesson_dir / "lesson.json"
    report = content_validator.validate_content(path_globs=(str(lesson_json),))
    if not report.ok:
        for issue in report.errors:
            console.print(f"ERROR: {issue.kind}: {issue.path}")
            console.print(f"  {issue.message}")
        raise click.ClickException("scaffolded lesson failed validation")
    relative_lesson_dir = lesson_dir
    try:
        relative_lesson_dir = lesson_dir.relative_to(paths.REPO_ROOT)
    except ValueError:
        pass
    _success(f"created {relative_lesson_dir}")


@main.group(help="Run review engine commands.")
def review() -> None:
    """Run review engine commands."""


@review.command("run", help="Run the review engine; implemented in PROMPT_27.")
def review_run() -> None:
    """Run the review engine; implemented in PROMPT_27."""
    _success("review engine lands in PROMPT_27")


@main.group(help="Run decision-engine commands.")
def decision() -> None:
    """Run decision-engine commands."""


@decision.command("run", help="Run the decision engine; implemented in PROMPT_43.")
def decision_run() -> None:
    """Run the decision engine; implemented in PROMPT_43."""
    _success("decision engine lands in PROMPT_43")


@main.group(help="Run interview simulator commands.")
def interview() -> None:
    """Run interview simulator commands."""


@interview.command("start", help="Start the interview simulator; implemented in PROMPT_28.")
def interview_start() -> None:
    """Start the interview simulator; implemented in PROMPT_28."""
    _success("interview simulator lands in PROMPT_28")

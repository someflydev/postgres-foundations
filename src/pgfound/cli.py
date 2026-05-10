"""Click command surface for pgfound."""

import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

import pgfound
from pgfound import exercise as exercise_runner
from pgfound import paths
from pgfound import progress as progress_store
from pgfound.content import lint as content_linter
from pgfound.content import loader
from pgfound.content import scaffold as content_scaffold
from pgfound.content import seed as content_seed
from pgfound.content import seed_doctor as content_seed_doctor
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


@lab.command("reset-domain", help="Drop, recreate, and reseed one domain schema.")
@click.argument("domain")
def lab_reset_domain(domain: str) -> None:
    """Reset one teaching domain to its latest available seed phase."""
    try:
        plan = content_seed.plan_seed(domain=domain)
        content_seed.execute_seed(plan, reset=True, generate=True)
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    _success(f"reset {domain}: {len(plan.sql_files)} SQL file(s)")


@lab.command("snapshot", help="Create a pg_dump snapshot under tmp/snapshots.")
@click.argument("name")
def lab_snapshot(name: str) -> None:
    """Dump the current pgfound database to tmp/snapshots/<name>.dump."""
    snapshot_path = _snapshot_path(name)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "docker",
        "compose",
        "exec",
        "-T",
        "pg",
        "pg_dump",
        "-U",
        "pgfound",
        "-d",
        "pgfound",
        "-Fc",
    ]
    try:
        with snapshot_path.open("wb") as dump_file:
            subprocess.run(cmd, cwd=paths.DOCKER_DIR, check=True, stdout=dump_file)
    except subprocess.CalledProcessError as exc:
        raise click.ClickException(str(exc)) from exc
    _success(f"snapshot written: {snapshot_path.relative_to(paths.REPO_ROOT)}")


@lab.command("restore", help="Restore a pg_dump snapshot from tmp/snapshots.")
@click.argument("name")
def lab_restore(name: str) -> None:
    """Restore tmp/snapshots/<name>.dump into the pgfound database."""
    snapshot_path = _snapshot_path(name)
    if not snapshot_path.is_file():
        relative_path = snapshot_path.relative_to(paths.REPO_ROOT)
        raise click.ClickException(f"snapshot not found: {relative_path}")
    cmd = [
        "docker",
        "compose",
        "exec",
        "-T",
        "pg",
        "pg_restore",
        "--clean",
        "--if-exists",
        "--no-owner",
        "-U",
        "pgfound",
        "-d",
        "pgfound",
    ]
    try:
        with snapshot_path.open("rb") as dump_file:
            subprocess.run(cmd, cwd=paths.DOCKER_DIR, check=True, stdin=dump_file)
    except subprocess.CalledProcessError as exc:
        raise click.ClickException(str(exc)) from exc
    _success(f"restored snapshot: {snapshot_path.relative_to(paths.REPO_ROOT)}")


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


@content_scaffold_group.command("exercise", help="Scaffold a draft exercise.")
@click.option(
    "--lesson",
    required=True,
    help="Lesson path under lessons/, for example phase-01-sql-literacy-basics/cluster/slug.",
)
@click.option("--level", required=True, type=click.Choice(["a", "b", "c", "d", "A", "B", "C", "D"]))
@click.option("--slug", required=True, help="Exercise slug and ID.")
@click.option(
    "--kind",
    required=True,
    type=click.Choice(["query", "schema", "modeling", "debug", "critique", "lab"]),
)
@click.option("--title", required=True, help="Human-facing exercise title.")
def content_scaffold_exercise(
    lesson: str,
    level: str,
    slug: str,
    kind: str,
    title: str,
) -> None:
    """Scaffold a draft exercise and validate the generated file."""
    try:
        exercise_dir = content_scaffold.scaffold_exercise(
            lesson=lesson,
            level=level,
            slug=slug,
            kind=kind,
            title=title,
        )
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    exercise_json = exercise_dir / "exercise.json"
    lesson_json = paths.LESSONS_DIR / lesson / "lesson.json"
    report = content_validator.validate_content(
        path_globs=(
            str(lesson_json),
            str(exercise_json),
            str(paths.RUBRICS_DIR / "default" / "*.rubric.json"),
        ),
    )
    if not report.ok:
        for issue in report.errors:
            console.print(f"ERROR: {issue.kind}: {issue.path}")
            console.print(f"  {issue.message}")
        raise click.ClickException("scaffolded exercise failed validation")
    relative_exercise_dir = exercise_dir
    try:
        relative_exercise_dir = exercise_dir.relative_to(paths.REPO_ROOT)
    except ValueError:
        pass
    _success(f"created {relative_exercise_dir}")


@content.command("lint", help="Run lesson authoring lint checks.")
@click.option("--strict", is_flag=True, help="Exit non-zero when lint warnings are present.")
@click.option(
    "--paths",
    "path_globs",
    multiple=True,
    help="Restrict lint to a file glob. May be provided more than once.",
)
def content_lint(path_globs: tuple[str, ...], strict: bool) -> None:
    """Run heavier lesson authoring checks."""
    report = content_linter.lint_content(path_globs=path_globs)
    table = Table(title="pgfound content lint")
    table.add_column("Files", justify="right")
    table.add_column("Warnings", justify="right")
    table.add_row(str(report.files_checked), str(len(report.warnings)))
    console.print(table)

    for issue in report.warnings:
        relative = issue.path
        try:
            relative = issue.path.relative_to(paths.REPO_ROOT)
        except ValueError:
            pass
        console.print(f"WARNING: {issue.kind}: {relative}")
        console.print(f"  {issue.message}")

    if strict and report.warnings:
        raise click.ClickException(
            f"FAIL: checked {report.files_checked} file(s), {len(report.warnings)} warning(s)"
        )
    _success(f"PASS: checked {report.files_checked} file(s), {len(report.warnings)} warning(s)")


@content.command("seed", help="Load reusable domain seed data into the lab.")
@click.argument("domain")
@click.option("--phase", "phase_id", help="Run SQL up to this phase ID, for example 1 or 7b.")
@click.option("--reset", is_flag=True, help="Drop and recreate the domain schema before seeding.")
@click.option("--generate", is_flag=True, help="Run deterministic pack generators before seeding.")
@click.option("--dry-run", is_flag=True, help="Print the SQL files that would execute.")
def content_seed_command(
    domain: str, phase_id: str | None, reset: bool, generate: bool, dry_run: bool
) -> None:
    """Load a reusable teaching domain seed pack."""
    try:
        plan = content_seed.plan_seed(domain=domain, phase=phase_id)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    if dry_run:
        if reset:
            console.print(f"RESET: {content_seed.reset_schema_sql(domain)}")
        if generate:
            for generator in plan.generators:
                console.print(f"GENERATE: {generator.relative_to(paths.REPO_ROOT)}")
        for sql_file in plan.sql_files:
            console.print(sql_file.relative_to(paths.REPO_ROOT))
        _success(f"DRY RUN: {len(plan.sql_files)} SQL file(s)")
        return

    try:
        content_seed.execute_seed(plan, reset=reset, generate=generate)
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc

    _success(f"seeded {domain}: {len(plan.sql_files)} SQL file(s)")


@content.command("seed-doctor", help="Check exercise seed references and solution table use.")
def content_seed_doctor_command() -> None:
    """Run seed-data sufficiency checks across authored exercises."""
    report = content_seed_doctor.run_seed_doctor()
    table = Table(title="pgfound content seed-doctor")
    table.add_column("Exercise")
    table.add_column("Seed Pack")
    table.add_column("Phase")
    table.add_column("Issue")
    if report.issues:
        for issue in report.issues:
            table.add_row(issue.exercise_id, issue.seed_pack_id, issue.phase, issue.message)
    else:
        table.add_row("all", "-", "-", "no issues")
    console.print(table)

    if report.ok:
        _success(f"PASS: checked {report.exercises_checked} exercise(s)")
        return
    raise click.ClickException(
        f"FAIL: checked {report.exercises_checked} exercise(s), {len(report.issues)} issue(s)"
    )


@main.group(help="Run learner exercises.")
def exercise() -> None:
    """Run learner exercises."""


@exercise.command("run", help="Print an exercise prompt and open the lab psql session.")
@click.argument("exercise_id")
@click.option("--auto-seed", is_flag=True, help="Reset and load the exercise seed pack first.")
@click.option("--dry-run", is_flag=True, help="Print the prompt and seed plan without Docker.")
@click.option(
    "--check", is_flag=True, help="Compare tmp/answers/<exercise-id>.sql to solution.sql."
)
@click.option(
    "--answer",
    "answer_path",
    type=click.Path(path_type=Path),
    help="SQL answer path to check instead of tmp/answers/<exercise-id>.sql.",
)
@click.option("--no-prompt", is_flag=True, help="Skip printing the exercise prompt.")
@click.option(
    "--save-answer",
    is_flag=True,
    help="Best-effort copy of the last psql history statement to the canonical answer path.",
)
@click.option(
    "--timing",
    is_flag=True,
    help="With --check, report solution and answer execution time.",
)
def exercise_run(
    exercise_id: str,
    auto_seed: bool,
    dry_run: bool,
    check: bool,
    answer_path: Path | None,
    no_prompt: bool,
    save_answer: bool,
    timing: bool,
) -> None:
    """Run or check one exercise."""
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        record = exercise_runner.find_exercise(exercise_id)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    seed_lines = exercise_runner.seed_plan_lines(record)
    console.print(f"Exercise: {record.id}")
    console.print(f"Seed pack: {record.seed_domain} phase {record.seed_phase}")
    console.print(f"Search path: {record.search_path}")
    for line in seed_lines:
        console.print(f"SEED: {line}")
    if not no_prompt:
        prompt = record.prompt_path.read_text(encoding="utf-8")
        console.print("")
        console.print(prompt)

    if dry_run:
        _success(f"DRY RUN: would use {len(seed_lines)} seed SQL file(s)")
        return

    if auto_seed:
        try:
            exercise_runner.auto_seed(record)
        except Exception as exc:
            raise click.ClickException(str(exc)) from exc
        _success(f"seeded {record.seed_domain} phase {record.seed_phase}")

    if check:
        try:
            correct, diff, timings = exercise_runner.check_answer_with_timing(
                record,
                answer_path=answer_path,
                timing=timing,
            )
        except Exception as exc:
            raise click.ClickException(str(exc)) from exc
        check_result = "correct" if correct else "incorrect"
        progress_path = exercise_runner.save_attempt(
            record,
            started_at=started_at,
            check_result=check_result,
        )
        if timings:
            console.print(
                "Timing: "
                f"solution {timings['solution_seconds']:.4f}s, "
                f"answer {timings['answer_seconds']:.4f}s"
            )
        if correct:
            _success("correct")
            _success(f"recorded {progress_path.relative_to(paths.REPO_ROOT)}")
            return
        console.print("incorrect, diff follows")
        console.print(diff)
        raise click.ClickException("answer did not match reference output")

    if not auto_seed and not click.confirm("Open psql without auto-seeding first?", default=True):
        _success("stopped before psql")
        return

    try:
        exercise_runner.run_psql(search_path=record.search_path)
    except subprocess.CalledProcessError as exc:
        raise click.ClickException(str(exc)) from exc

    if save_answer:
        try:
            saved_path = exercise_runner.save_answer_from_history(record)
        except Exception as exc:
            console.print(f"WARNING: could not save answer from psql history: {exc}")
        else:
            _success(f"saved answer {saved_path.relative_to(paths.REPO_ROOT)}")

    assessment = "not_recorded"
    if click.confirm("Record a self-assessment for this exercise?", default=False):
        assessment = click.prompt("Self-assessment", default="not recorded")
    progress_path = exercise_runner.save_attempt(
        record,
        started_at=started_at,
        self_assessment=assessment,
    )
    _success(f"recorded {progress_path.relative_to(paths.REPO_ROOT)}")


@main.group(help="Show learner progress.")
def progress() -> None:
    """Show learner progress."""


@progress.command("show", help="Print a minimal tmp/progress summary.")
def progress_show() -> None:
    """Print a minimal learner progress summary."""
    summary = progress_store.summarize()
    table = Table(title="pgfound progress")
    table.add_column("Area")
    table.add_column("Files", justify="right")
    table.add_column("Attempts", justify="right")
    table.add_row("profile", "1" if summary.profile_exists else "0", "-")
    table.add_row("exercises", str(summary.exercise_files), str(summary.exercise_attempts))
    table.add_row("capstones", str(summary.capstone_files), str(summary.capstone_attempts))
    console.print(table)


def _snapshot_path(name: str) -> Path:
    if "/" in name or "\\" in name or name in {"", ".", ".."}:
        raise click.ClickException("snapshot name must be a simple file stem")
    return paths.REPO_ROOT / "tmp" / "snapshots" / f"{name}.dump"


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

"""Click command surface for pgfound."""

import json
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
from pgfound.lab import explain as lab_explain
from pgfound.lab import harness as concurrency_harness
from pgfound.review import engine as review_engine
from pgfound.review.models import EvaluationContext, EvaluationRequest
from pgfound.review.output import report as review_report

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


@lab.command("explain", help="Run EXPLAIN ANALYZE and print a simplified plan tree.")
@click.argument("sql_file_or_inline", required=False)
@click.option("--baseline", help="Save the current plan under tmp/plans/<label>.json.")
@click.option("--compare", "compare_label", help="Compare with a saved plan label.")
def lab_explain_command(
    sql_file_or_inline: str | None,
    baseline: str | None,
    compare_label: str | None,
) -> None:
    """Run or compare JSON EXPLAIN plans for the lab database."""
    try:
        sql = lab_explain.read_sql(sql_file_or_inline)
        if sql is None:
            if not baseline or not compare_label:
                raise click.ClickException(
                    "provide SQL, or provide both --baseline and --compare to diff saved plans"
                )
            before = lab_explain.load_plan(baseline)
            after = lab_explain.load_plan(compare_label)
            lab_explain.render_diff(console, before, after)
            return

        current = lab_explain.explain_sql(sql)
        lab_explain.render_plan(console, current, sql=sql)
        if compare_label:
            before = lab_explain.load_plan(compare_label)
            lab_explain.render_diff(console, before, current)
        if baseline:
            path = lab_explain.save_plan(baseline, current)
            _success(f"saved plan: {path.relative_to(paths.REPO_ROOT)}")
    except click.ClickException:
        raise
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc


@lab.group("concurrency", help="Run deterministic multi-session lab scenarios.")
def lab_concurrency() -> None:
    """Run deterministic multi-session lab scenarios."""


@lab_concurrency.command("list", help="List concurrency scenario YAML files.")
def lab_concurrency_list() -> None:
    """List concurrency scenario YAML files."""
    table = Table(title="pgfound concurrency scenarios")
    table.add_column("Scenario")
    table.add_column("Path")
    for scenario_path in concurrency_harness.scenario_paths():
        table.add_row(scenario_path.stem, str(scenario_path.relative_to(paths.REPO_ROOT)))
    console.print(table)


@lab_concurrency.command("run", help="Run one concurrency scenario YAML file.")
@click.argument("scenario_yaml", type=click.Path(path_type=Path))
@click.option(
    "--on-fail",
    type=click.Choice(["close", "pause"]),
    default="close",
    show_default=True,
    help=(
        "Failure handling mode. pause currently prints diagnostics before closing harness sessions."
    ),
)
def lab_concurrency_run(scenario_yaml: Path, on_fail: str) -> None:
    """Run one concurrency scenario YAML file."""
    try:
        scenario_path = concurrency_harness.find_scenario(scenario_yaml)
        report = concurrency_harness.run_scenario_path(
            scenario_path,
            pause_on_failure=on_fail == "pause",
        )
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    _print_harness_report(report)
    if report.ok:
        _success("concurrency scenario passed")
        return
    raise click.ClickException("concurrency scenario failed")


@lab_concurrency.command("record", help="Run a scenario and emit a normalized transcript.")
@click.argument("scenario_yaml", type=click.Path(path_type=Path))
def lab_concurrency_record(scenario_yaml: Path) -> None:
    """Run one scenario and print a normalized JSON transcript."""
    try:
        scenario_path = concurrency_harness.find_scenario(scenario_yaml)
        report = concurrency_harness.run_scenario_path(scenario_path)
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    console.print(concurrency_harness.normalized_transcript(report), end="")
    if not report.ok:
        raise click.ClickException("concurrency scenario failed")


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
@click.option(
    "--sessions",
    default=1,
    show_default=True,
    type=click.IntRange(min=1),
    help="Number of psql sessions needed by a multi-session exercise.",
)
def content_scaffold_exercise(
    lesson: str,
    level: str,
    slug: str,
    kind: str,
    title: str,
    sessions: int,
) -> None:
    """Scaffold a draft exercise and validate the generated file."""
    try:
        exercise_dir = content_scaffold.scaffold_exercise(
            lesson=lesson,
            level=level,
            slug=slug,
            kind=kind,
            title=title,
            sessions=sessions,
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


@exercise.command("review", help="Review an exercise answer and write reports.")
@click.argument("exercise_id")
@click.option(
    "--answer",
    "answer_path",
    type=click.Path(path_type=Path),
    required=True,
    help="SQL answer path to review.",
)
@click.option("--auto", "mode_auto", is_flag=True, help="Run mechanical checks only.")
@click.option("--full", "mode_full", is_flag=True, help="Run all available mechanical checks.")
def exercise_review(
    exercise_id: str,
    answer_path: Path,
    mode_auto: bool,
    mode_full: bool,
) -> None:
    """Review one exercise answer."""
    mode = "full" if mode_full else "auto"
    if mode_auto and mode_full:
        raise click.ClickException("choose only one of --auto or --full")
    request = EvaluationRequest(
        target_id=exercise_id,
        artifact_path=answer_path,
        context=EvaluationContext(repo_root=paths.REPO_ROOT, db_url=content_seed.database_url()),
        mode=mode,
        target_kind="exercise",
    )
    try:
        result = review_engine.evaluate(request)
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    review_report.render_console(console, result)
    _success(f"markdown: {result.report_paths['markdown']}")
    _success(f"json: {result.report_paths['json']}")


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


@main.group(help="Run capstone workspace commands.")
def capstone() -> None:
    """Run capstone workspace commands."""


@capstone.command("start", help="Copy a capstone starter workspace and print its brief.")
@click.argument("capstone_id")
def capstone_start(capstone_id: str) -> None:
    """Start a capstone attempt."""
    capstone_dir = paths.CAPSTONES_DIR / capstone_id
    starter_dir = capstone_dir / "starter"
    if not starter_dir.is_dir():
        raise click.ClickException(f"capstone starter not found: {capstone_id}")

    work_dir = paths.TMP_DIR / "capstone-work" / capstone_id
    if work_dir.exists():
        shutil.rmtree(work_dir)
    shutil.copytree(starter_dir, work_dir)

    started_at = datetime.now(timezone.utc).isoformat()
    progress_path = progress_store.capstone_progress_path(capstone_id)
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    if progress_path.is_file():
        payload = json.loads(progress_path.read_text(encoding="utf-8"))
    else:
        payload = {"capstone_id": capstone_id, "attempts": []}
    attempts = payload.setdefault("attempts", [])
    if not isinstance(attempts, list):
        raise click.ClickException(f"invalid capstone progress record: {progress_path}")
    attempts.append(
        {
            "started_at": started_at,
            "workspace": str(work_dir.relative_to(paths.REPO_ROOT)),
            "status": "started",
        }
    )
    progress_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for name in ("brief.md", "constraints.md", "acceptance-criteria.md"):
        path = capstone_dir / name
        if path.is_file():
            console.print(path.read_text(encoding="utf-8").rstrip())
            console.print("")
    _success(f"workspace: {work_dir.relative_to(paths.REPO_ROOT)}")
    _success(f"recorded: {progress_path.relative_to(paths.REPO_ROOT)}")


@capstone.command("evaluate", help="Evaluate a capstone submission.")
@click.argument("capstone_id")
@click.option("--path", "submission_path", type=click.Path(path_type=Path), required=True)
@click.option("--full", "mode_full", is_flag=True, help="Run all available mechanical checks.")
def capstone_evaluate(capstone_id: str, submission_path: Path, mode_full: bool) -> None:
    """Evaluate a capstone submission."""
    request = EvaluationRequest(
        target_id=capstone_id,
        artifact_path=submission_path,
        context=EvaluationContext(
            repo_root=paths.REPO_ROOT,
            db_url=content_seed.sandbox_database_url() if mode_full else None,
        ),
        mode="full" if mode_full else "auto",
        target_kind="capstone",
    )
    try:
        result = review_engine.evaluate(request)
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    review_report.render_console(console, result)
    _success(f"markdown: {result.report_paths['markdown']}")
    _success(f"json: {result.report_paths['json']}")


def _snapshot_path(name: str) -> Path:
    if "/" in name or "\\" in name or name in {"", ".", ".."}:
        raise click.ClickException("snapshot name must be a simple file stem")
    return paths.REPO_ROOT / "tmp" / "snapshots" / f"{name}.dump"


def _print_harness_report(report: concurrency_harness.HarnessReport) -> None:
    table = Table(title=f"concurrency: {report.scenario_name}")
    table.add_column("#", justify="right")
    table.add_column("Session")
    table.add_column("Status")
    table.add_column("SQL")
    for entry in report.transcript:
        sql = " ".join(entry.sql.strip().split())
        if len(sql) > 76:
            sql = sql[:73] + "..."
        table.add_row(str(entry.index), entry.session, entry.status, sql)
    console.print(table)
    if report.diff:
        console.print(report.diff)


@main.group(help="Run review engine commands.")
def review() -> None:
    """Run review engine commands."""


@review.command("run", help="Run the review engine for an exercise or capstone.")
@click.option("--exercise-id", help="Exercise ID to review.")
@click.option("--capstone-id", help="Capstone ID to review.")
@click.option(
    "--answer", "answer_path", type=click.Path(path_type=Path), help="Exercise answer path."
)
@click.option(
    "--path", "artifact_path", type=click.Path(path_type=Path), help="Capstone attempt directory."
)
@click.option("--full", "mode_full", is_flag=True, help="Run all available mechanical checks.")
def review_run(
    exercise_id: str | None,
    capstone_id: str | None,
    answer_path: Path | None,
    artifact_path: Path | None,
    mode_full: bool,
) -> None:
    """Run the review engine."""
    if bool(exercise_id) == bool(capstone_id):
        raise click.ClickException("provide exactly one of --exercise-id or --capstone-id")
    target_kind = "exercise" if exercise_id else "capstone"
    target_id = exercise_id or capstone_id
    artifact = answer_path if exercise_id else artifact_path
    if target_id is None or artifact is None:
        raise click.ClickException("exercise reviews need --answer; capstone reviews need --path")
    db_url = content_seed.database_url() if exercise_id else None
    if capstone_id and mode_full:
        db_url = content_seed.sandbox_database_url()
    request = EvaluationRequest(
        target_id=target_id,
        artifact_path=artifact,
        context=EvaluationContext(repo_root=paths.REPO_ROOT, db_url=db_url),
        mode="full" if mode_full else "auto",
        target_kind=target_kind,
    )
    try:
        result = review_engine.evaluate(request)
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    review_report.render_console(console, result)
    _success(f"markdown: {result.report_paths['markdown']}")
    _success(f"json: {result.report_paths['json']}")


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

"""Deterministic multi-session PostgreSQL concurrency harness."""

from __future__ import annotations

import difflib
import json
import queue
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import psycopg
import yaml

from pgfound import paths
from pgfound.content import seed as content_seed
from pgfound.review.normalize import normalize_for_comparison

DEFAULT_TIMEOUT_SECONDS = 2.0
BLOCK_TIMEOUT_SECONDS = 0.5
LEARNER_SQL_PLACEHOLDER = "${LEARNER_SQL}"


@dataclass(frozen=True)
class StepResult:
    """Result from one SQL step."""

    session: str
    sql: str
    rows: list[dict[str, Any]] = field(default_factory=list)
    rowcount: int = -1
    error_code: str | None = None
    error_message: str = ""
    seconds: float = 0.0


@dataclass(frozen=True)
class TranscriptEntry:
    """Printable transcript entry."""

    index: int
    session: str
    sql: str
    status: str
    result: StepResult | None = None
    detail: str = ""


@dataclass(frozen=True)
class HarnessReport:
    """Final harness report."""

    scenario_name: str
    ok: bool
    transcript: list[TranscriptEntry]
    diff: str = ""


@dataclass
class _Task:
    sql: str
    outbox: queue.Queue[StepResult]


class HarnessMismatch(Exception):
    """Raised when a scenario expectation does not match observed behavior."""

    def __init__(self, message: str, diff: str = "") -> None:
        super().__init__(message)
        self.diff = diff


class _SessionWorker:
    def __init__(self, name: str, spec: dict[str, Any]) -> None:
        self.name = name
        self.spec = spec
        self.inbox: queue.Queue[_Task | None] = queue.Queue()
        self.connection: psycopg.Connection[Any] | None = None
        self.thread = threading.Thread(target=self._run, name=f"pgfound-harness-{name}")
        self.thread.daemon = True

    def start(self) -> None:
        self.thread.start()

    def dispatch(self, sql: str) -> queue.Queue[StepResult]:
        outbox: queue.Queue[StepResult] = queue.Queue(maxsize=1)
        self.inbox.put(_Task(sql=sql, outbox=outbox))
        return outbox

    def close(self) -> None:
        self.inbox.put(None)
        self.thread.join(timeout=2)
        if self.connection is not None:
            self.connection.close()

    def _run(self) -> None:
        role = str(self.spec.get("role", "pgfound"))
        database = str(self.spec.get("database", "pgfound"))
        dsn = _database_url(role=role, database=database)
        self.connection = psycopg.connect(dsn, autocommit=False)
        while True:
            task = self.inbox.get()
            if task is None:
                return
            task.outbox.put(_execute_sql(self.connection, self.name, task.sql))


def scenario_paths() -> list[Path]:
    """Return all concurrency scenario YAML paths."""
    root = paths.SCENARIOS_DIR / "concurrency"
    if not root.is_dir():
        return []
    return sorted((*root.rglob("*.yaml"), *root.rglob("*.yml")))


def find_scenario(slug_or_path: str | Path) -> Path:
    """Resolve a scenario slug or YAML path."""
    path = Path(slug_or_path)
    candidates: list[Path] = []
    if path.is_file():
        return path
    repo_path = paths.REPO_ROOT / path
    if repo_path.is_file():
        return repo_path
    for scenario_path in scenario_paths():
        if scenario_path.stem == str(slug_or_path):
            candidates.append(scenario_path)
    if not candidates:
        msg = f"scenario not found: {slug_or_path}"
        raise ValueError(msg)
    if len(candidates) > 1:
        msg = f"scenario is ambiguous: {slug_or_path}"
        raise ValueError(msg)
    return candidates[0]


def load_scenario(path: Path, *, learner_sql: str | None = None) -> dict[str, Any]:
    """Load a YAML scenario, optionally substituting learner SQL."""
    text = path.read_text(encoding="utf-8")
    if learner_sql is not None:
        if LEARNER_SQL_PLACEHOLDER not in text:
            msg = f"scenario has no {LEARNER_SQL_PLACEHOLDER} placeholder: {_relative_path(path)}"
            raise ValueError(msg)
    parsed = yaml.safe_load(text) or {}
    if not isinstance(parsed, dict):
        msg = f"scenario must be a YAML mapping: {_relative_path(path)}"
        raise ValueError(msg)
    if learner_sql is not None:
        parsed = _replace_learner_sql(parsed, learner_sql)
    validate_scenario(parsed, source=path)
    return parsed


def validate_scenario(scenario: dict[str, Any], *, source: Path | None = None) -> None:
    """Validate the harness-level scenario shape."""
    location = f" in {_relative_path(source)}" if source else ""
    sessions = scenario.get("sessions")
    steps = scenario.get("steps")
    if not isinstance(scenario.get("name"), str) or not scenario["name"]:
        raise ValueError(f"scenario name is required{location}")
    if not isinstance(sessions, dict) or not sessions:
        raise ValueError(f"scenario sessions must be a non-empty mapping{location}")
    if not isinstance(steps, list) or not steps:
        raise ValueError(f"scenario steps must be a non-empty list{location}")
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise ValueError(f"step {index} must be a mapping{location}")
        session = step.get("session")
        if session not in sessions:
            raise ValueError(f"step {index} references undeclared session {session!r}{location}")
        if not isinstance(step.get("sql"), str) or not step["sql"].strip():
            raise ValueError(f"step {index} sql is required{location}")


def run_scenario_path(
    path: Path, *, learner_sql: str | None = None, pause_on_failure: bool = False
) -> HarnessReport:
    """Load and run a scenario file."""
    scenario = load_scenario(path, learner_sql=learner_sql)
    return run_scenario(scenario, pause_on_failure=pause_on_failure)


def run_scenario(scenario: dict[str, Any], *, pause_on_failure: bool = False) -> HarnessReport:
    """Execute a loaded scenario."""
    transcript: list[TranscriptEntry] = []
    workers: dict[str, _SessionWorker] = {}
    pending: dict[str, tuple[int, dict[str, Any], queue.Queue[StepResult]]] = {}
    name = str(scenario["name"])

    try:
        _run_scratch_sql(str(scenario.get("setup_sql", "")).strip())
        workers = {
            session: _SessionWorker(session, spec if isinstance(spec, dict) else {})
            for session, spec in scenario["sessions"].items()
        }
        for worker in workers.values():
            worker.start()

        for index, step in enumerate(scenario["steps"], start=1):
            session = str(step["session"])
            if session in pending:
                _resolve_pending(session, pending, transcript)
            timeout = float(step.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
            expect = step.get("expect", {})
            expect = expect if isinstance(expect, dict) else {}
            outbox = workers[session].dispatch(str(step["sql"]))
            if expect.get("blocks") is True:
                block_timeout = float(step.get("timeout_seconds", BLOCK_TIMEOUT_SECONDS))
                try:
                    result = outbox.get(timeout=block_timeout)
                except queue.Empty:
                    pending[session] = (index, step, outbox)
                    transcript.append(TranscriptEntry(index, session, str(step["sql"]), "blocked"))
                    continue
                raise HarnessMismatch(
                    f"step {index} session {session} completed but expected to block",
                    _diff_expected_actual({"blocks": True}, _result_payload(result)),
                )
            result = outbox.get(timeout=timeout)
            _assert_expectation(index, step, result)
            transcript.append(TranscriptEntry(index, session, str(step["sql"]), "ok", result))

        for session in list(pending):
            _resolve_pending(session, pending, transcript)
    except (HarnessMismatch, queue.Empty) as exc:
        diff = exc.diff if isinstance(exc, HarnessMismatch) else str(exc)
        if pause_on_failure:
            input(
                "Scenario failed. Harness connections are still open; "
                "inspect from another psql, then press Enter to close them."
            )
        return HarnessReport(name, False, transcript, diff=diff)
    finally:
        for worker in workers.values():
            worker.close()
        _run_scratch_sql(str(scenario.get("teardown_sql", "")).strip())

    return HarnessReport(name, True, transcript)


def normalized_transcript(report: HarnessReport) -> str:
    """Return a stable JSON transcript."""
    payload = {
        "scenario": report.scenario_name,
        "ok": report.ok,
        "steps": [
            {
                "index": entry.index,
                "session": entry.session,
                "status": entry.status,
                "sql": entry.sql,
                "result": _result_payload(entry.result) if entry.result else None,
                "detail": entry.detail,
            }
            for entry in report.transcript
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _resolve_pending(
    session: str,
    pending: dict[str, tuple[int, dict[str, Any], queue.Queue[StepResult]]],
    transcript: list[TranscriptEntry],
) -> None:
    index, step, outbox = pending.pop(session)
    timeout = float(step.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
    result = outbox.get(timeout=timeout)
    transcript.append(TranscriptEntry(index, session, str(step["sql"]), "unblocked", result))


def _execute_sql(
    connection: psycopg.Connection[Any],
    session: str,
    sql: str,
) -> StepResult:
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    rowcount = -1
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            while True:
                if cursor.description is not None:
                    columns = [column.name for column in cursor.description]
                    rows = [
                        {
                            column: normalize_for_comparison(value)
                            for column, value in zip(columns, row, strict=True)
                        }
                        for row in cursor.fetchall()
                    ]
                if cursor.rowcount >= 0:
                    rowcount = cursor.rowcount
                if not cursor.nextset():
                    break
        return StepResult(
            session,
            sql,
            rows=rows,
            rowcount=rowcount,
            seconds=time.perf_counter() - started,
        )
    except psycopg.Error as exc:
        connection.rollback()
        return StepResult(
            session,
            sql,
            rowcount=rowcount,
            error_code=exc.sqlstate,
            error_message=str(exc).strip(),
            seconds=time.perf_counter() - started,
        )


def _assert_expectation(index: int, step: dict[str, Any], result: StepResult) -> None:
    expect = step.get("expect", {})
    if not isinstance(expect, dict):
        return
    if "error_code" in expect:
        if result.error_code != str(expect["error_code"]):
            raise HarnessMismatch(
                f"step {index} expected SQLSTATE {expect['error_code']}, got {result.error_code}",
                _diff_expected_actual(expect, _result_payload(result)),
            )
        return
    if result.error_code is not None:
        raise HarnessMismatch(
            f"step {index} raised unexpected SQLSTATE {result.error_code}",
            _diff_expected_actual(expect, _result_payload(result)),
        )
    if "rowcount" in expect and result.rowcount != int(expect["rowcount"]):
        raise HarnessMismatch(
            f"step {index} expected rowcount {expect['rowcount']}, got {result.rowcount}",
            _diff_expected_actual(expect, _result_payload(result)),
        )
    if "rows" in expect:
        expected_rows = [_normalize_row(row) for row in expect["rows"]]
        actual_rows = [_normalize_row(row) for row in result.rows]
        if expect.get("ordered") is not True:
            expected_rows = sorted(expected_rows, key=json.dumps)
            actual_rows = sorted(actual_rows, key=json.dumps)
        if actual_rows != expected_rows:
            raise HarnessMismatch(
                f"step {index} rows did not match",
                _diff_expected_actual({"rows": expected_rows}, {"rows": actual_rows}),
            )


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {str(key): normalize_for_comparison(value) for key, value in row.items()}


def _result_payload(result: StepResult | None) -> dict[str, Any]:
    if result is None:
        return {}
    return {
        "rows": result.rows,
        "rowcount": result.rowcount,
        "error_code": result.error_code,
        "error_message": result.error_message,
    }


def _diff_expected_actual(expected: dict[str, Any], actual: dict[str, Any]) -> str:
    expected_lines = json.dumps(expected, indent=2, sort_keys=True).splitlines()
    actual_lines = json.dumps(actual, indent=2, sort_keys=True).splitlines()
    return "\n".join(
        difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


def _run_scratch_sql(sql: str) -> None:
    if not sql:
        return
    with psycopg.connect(content_seed.database_url(), autocommit=True) as connection:
        connection.execute(sql)


def _database_url(*, role: str, database: str) -> str:
    base = content_seed.database_url()
    if role == "pgfound" and database == "pgfound":
        return base
    connection = psycopg.conninfo.conninfo_to_dict(base)
    connection["user"] = role
    connection["dbname"] = database
    return psycopg.conninfo.make_conninfo(**connection)


def _relative_path(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return str(path.relative_to(paths.REPO_ROOT))
    except ValueError:
        return str(path)


def _replace_learner_sql(value: Any, learner_sql: str) -> Any:
    if isinstance(value, str):
        return value.replace(LEARNER_SQL_PLACEHOLDER, learner_sql)
    if isinstance(value, list):
        return [_replace_learner_sql(item, learner_sql) for item in value]
    if isinstance(value, dict):
        return {key: _replace_learner_sql(item, learner_sql) for key, item in value.items()}
    return value

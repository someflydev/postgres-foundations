"""Seed-data pack discovery and execution."""

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import psycopg

from pgfound import paths
from pgfound.config import load_config

PHASE_FILE_RE = re.compile(r"^phase-(?P<phase>\d+[a-z]?)\.sql$")

SCHEMA_BY_DOMAIN = {
    "ecommerce": "ecommerce",
    "scheduling": "scheduling",
    "saas_multi_tenant": "saas",
    "event_heavy_ops": "events",
    "document_search": "documents",
    "modernization_bridge": "legacy",
}


@dataclass(frozen=True)
class SeedPlan:
    domain: str
    sql_files: tuple[Path, ...]
    generators: tuple[Path, ...]


def database_url() -> str:
    """Return the lab database URL from env or compose defaults."""
    env_url = os.environ.get("PGFOUND_DB_URL")
    if env_url:
        return env_url

    config = load_config()
    return (
        "postgresql://"
        f"{config.postgres_user}:{config.postgres_password}"
        f"@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
    )


def phase_sort_key(phase: str) -> tuple[int, int, str]:
    """Sort plain and lettered curriculum phases in teaching order."""
    match = re.fullmatch(r"(?P<number>\d+)(?P<suffix>[a-z]?)", phase)
    if match is None:
        msg = f"invalid phase id: {phase}"
        raise ValueError(msg)
    suffix = match.group("suffix")
    suffix_order = 0 if not suffix else ord(suffix) - ord("a") + 1
    return (int(match.group("number")), suffix_order, suffix)


def _pack_dir(domain: str) -> Path:
    pack_dir = paths.SEED_DATA_DIR / "packs" / domain
    if not pack_dir.is_dir():
        msg = f"unknown seed domain: {domain}"
        raise ValueError(msg)
    return pack_dir


def _phase_from_path(path: Path) -> str:
    match = PHASE_FILE_RE.match(path.name)
    if match is None:
        msg = f"invalid phase SQL filename: {path.name}"
        raise ValueError(msg)
    return match.group("phase")


def plan_seed(domain: str, phase: str | None = None) -> SeedPlan:
    """Build the ordered list of generators and SQL files for a seed request."""
    pack_dir = _pack_dir(domain)
    phase_dir = pack_dir / "phases"
    sql_files = sorted(
        (path for path in phase_dir.glob("phase-*.sql") if PHASE_FILE_RE.match(path.name)),
        key=lambda path: phase_sort_key(_phase_from_path(path)),
    )

    if phase is not None:
        requested_key = phase_sort_key(phase)
        sql_files = [
            path for path in sql_files if phase_sort_key(_phase_from_path(path)) <= requested_key
        ]

    generator_dir = pack_dir / "generators"
    generators = (
        tuple(sorted(generator_dir.glob("*.py"), key=lambda path: path.name))
        if generator_dir.is_dir()
        else ()
    )
    return SeedPlan(domain=domain, sql_files=tuple(sql_files), generators=generators)


def reset_schema_sql(domain: str) -> str:
    """Return SQL that drops and recreates the canonical schema for a domain."""
    schema = SCHEMA_BY_DOMAIN.get(domain)
    if schema is None:
        msg = f"no schema mapping for seed domain: {domain}"
        raise ValueError(msg)
    return f'DROP SCHEMA IF EXISTS "{schema}" CASCADE; CREATE SCHEMA "{schema}";'


def run_generators(generators: tuple[Path, ...]) -> None:
    """Run deterministic pack generators and discard their stdout for now."""
    for generator in generators:
        subprocess.run(
            [sys.executable, str(generator)],
            check=True,
            capture_output=True,
            text=True,
        )


def execute_seed(plan: SeedPlan, *, reset: bool, generate: bool) -> None:
    """Execute a seed plan against the configured PostgreSQL lab."""
    if generate:
        run_generators(plan.generators)

    with psycopg.connect(database_url(), autocommit=True) as connection:
        if reset:
            connection.execute(reset_schema_sql(plan.domain))
        for sql_file in plan.sql_files:
            connection.execute(sql_file.read_text(encoding="utf-8"))

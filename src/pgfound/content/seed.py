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
    "logistics_geo": "logistics",
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


def sandbox_database_url() -> str:
    """Return the sandbox database URL from env or compose defaults."""
    env_url = os.environ.get("PGFOUND_SANDBOX_DB_URL")
    if env_url:
        return env_url

    config = load_config()
    return (
        "postgresql://"
        f"{config.postgres_user}:{config.postgres_password}"
        f"@{config.postgres_host}:{config.postgres_sandbox_port}/{config.postgres_db}"
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
            if phase_sort_key(_phase_from_path(sql_file)) == phase_sort_key("7a"):
                load_generated_phase_7a(connection, plan.domain)


def generated_phase_dir(domain: str, phase: str = "phase-07a") -> Path:
    """Return the cache directory for generated seed artifacts."""
    return paths.TMP_DIR / "generated-seed-data" / domain / phase


def load_generated_phase_7a(connection: psycopg.Connection, domain: str) -> None:
    """COPY generated phase 7a fixtures and merge them into canonical tables."""
    if domain == "ecommerce":
        _load_ecommerce_phase_7a(connection)
        return
    if domain == "scheduling":
        _load_scheduling_phase_7a(connection)


def _require_generated_file(domain: str, filename: str) -> Path:
    path = generated_phase_dir(domain) / filename
    if not path.is_file():
        relative = path.relative_to(paths.REPO_ROOT)
        msg = f"generated seed file missing: {relative}; rerun with --generate"
        raise FileNotFoundError(msg)
    return path


def _copy_csv(
    connection: psycopg.Connection,
    *,
    table: str,
    columns: tuple[str, ...],
    path: Path,
) -> None:
    column_list = ", ".join(columns)
    with path.open("rb") as csv_file:
        with connection.cursor() as cursor:
            with cursor.copy(
                f"COPY {table} ({column_list}) FROM STDIN WITH (FORMAT CSV, HEADER)"
            ) as copy:
                while chunk := csv_file.read(1024 * 1024):
                    copy.write(chunk)


def _load_ecommerce_phase_7a(connection: psycopg.Connection) -> None:
    connection.execute("TRUNCATE ecommerce.phase_07a_products_stage")
    connection.execute("TRUNCATE ecommerce.phase_07a_customers_stage")
    connection.execute("TRUNCATE ecommerce.phase_07a_orders_stage")
    connection.execute("TRUNCATE ecommerce.phase_07a_order_items_stage")

    _copy_csv(
        connection,
        table="ecommerce.phase_07a_products_stage",
        columns=("sku", "name", "price", "stock_on_hand", "created_at"),
        path=_require_generated_file("ecommerce", "products.csv"),
    )
    _copy_csv(
        connection,
        table="ecommerce.phase_07a_customers_stage",
        columns=("email", "full_name", "created_at"),
        path=_require_generated_file("ecommerce", "customers.csv"),
    )
    _copy_csv(
        connection,
        table="ecommerce.phase_07a_orders_stage",
        columns=("customer_email", "order_number", "status", "total_amount", "placed_at"),
        path=_require_generated_file("ecommerce", "orders.csv"),
    )
    _copy_csv(
        connection,
        table="ecommerce.phase_07a_order_items_stage",
        columns=("order_number", "sku", "quantity", "unit_price", "created_at"),
        path=_require_generated_file("ecommerce", "order_items.csv"),
    )

    connection.execute(
        """
        INSERT INTO ecommerce.products (sku, name, price, stock_on_hand, created_at, updated_at)
        SELECT sku, name, price, stock_on_hand, created_at, created_at
        FROM ecommerce.phase_07a_products_stage
        ON CONFLICT (sku) DO UPDATE
        SET name = EXCLUDED.name,
            price = EXCLUDED.price,
            stock_on_hand = EXCLUDED.stock_on_hand,
            updated_at = EXCLUDED.updated_at
        """
    )
    connection.execute(
        """
        INSERT INTO ecommerce.customers (email, full_name, created_at, updated_at)
        SELECT email, full_name, created_at, created_at
        FROM ecommerce.phase_07a_customers_stage
        ON CONFLICT (email) DO UPDATE
        SET full_name = EXCLUDED.full_name,
            updated_at = EXCLUDED.updated_at
        """
    )
    connection.execute(
        """
        INSERT INTO ecommerce.orders (
            customer_id, order_number, status, total_amount, placed_at, created_at, updated_at
        )
        SELECT c.id, s.order_number, s.status, s.total_amount, s.placed_at, s.placed_at, s.placed_at
        FROM ecommerce.phase_07a_orders_stage s
        JOIN ecommerce.customers c ON c.email = s.customer_email
        ON CONFLICT (order_number) DO UPDATE
        SET status = EXCLUDED.status,
            total_amount = EXCLUDED.total_amount,
            updated_at = EXCLUDED.updated_at
        """
    )
    connection.execute(
        """
        INSERT INTO ecommerce.order_items (
            order_id, product_id, quantity, unit_price, created_at, updated_at
        )
        SELECT o.id, p.id, s.quantity, s.unit_price, s.created_at, s.created_at
        FROM ecommerce.phase_07a_order_items_stage s
        JOIN ecommerce.orders o ON o.order_number = s.order_number
        JOIN ecommerce.products p ON p.sku = s.sku
        WHERE NOT EXISTS (
            SELECT 1
            FROM ecommerce.order_items existing
            WHERE existing.order_id = o.id
              AND existing.product_id = p.id
              AND existing.created_at = s.created_at
        )
        """
    )
    connection.execute("ANALYZE ecommerce.products")
    connection.execute("ANALYZE ecommerce.customers")
    connection.execute("ANALYZE ecommerce.orders")
    connection.execute("ANALYZE ecommerce.order_items")


def _load_scheduling_phase_7a(connection: psycopg.Connection) -> None:
    connection.execute("TRUNCATE scheduling.phase_07a_clients_stage")
    connection.execute("TRUNCATE scheduling.phase_07a_appointments_stage")

    _copy_csv(
        connection,
        table="scheduling.phase_07a_clients_stage",
        columns=("email", "full_name", "created_at"),
        path=_require_generated_file("scheduling", "clients.csv"),
    )
    _copy_csv(
        connection,
        table="scheduling.phase_07a_appointments_stage",
        columns=("professional_name", "client_email", "starts_at", "ends_at", "status"),
        path=_require_generated_file("scheduling", "appointments.csv"),
    )

    connection.execute(
        """
        INSERT INTO scheduling.clients (email, full_name, created_at, updated_at)
        SELECT email, full_name, created_at, created_at
        FROM scheduling.phase_07a_clients_stage
        ON CONFLICT (email) DO UPDATE
        SET full_name = EXCLUDED.full_name,
            updated_at = EXCLUDED.updated_at
        """
    )
    connection.execute(
        """
        INSERT INTO scheduling.appointments (
            provider_id, client_id, starts_at, ends_at, status, created_at, updated_at
        )
        SELECT p.id, c.id, s.starts_at, s.ends_at, s.status, s.starts_at, s.starts_at
        FROM scheduling.phase_07a_appointments_stage s
        JOIN scheduling.professionals p ON p.display_name = s.professional_name
        JOIN scheduling.clients c ON c.email = s.client_email
        ON CONFLICT (provider_id, starts_at) DO UPDATE
        SET client_id = EXCLUDED.client_id,
            ends_at = EXCLUDED.ends_at,
            status = EXCLUDED.status,
            updated_at = EXCLUDED.updated_at
        """
    )
    connection.execute("ANALYZE scheduling.clients")
    connection.execute("ANALYZE scheduling.appointments")

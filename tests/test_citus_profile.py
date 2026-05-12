from pathlib import Path

import yaml

COMPOSE_FILE = Path("docker/docker-compose.yml")


def load_compose() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text())


def test_citus_profile_references_pinned_cluster_images() -> None:
    compose = load_compose()
    services = compose["services"]

    for service_name in ("citus-coordinator", "citus-worker-1", "citus-worker-2"):
        service = services[service_name]
        assert service["image"] == "citusdata/citus:12.1"
        assert service["profiles"] == ["citus"]

    coordinator = services["citus-coordinator"]
    assert "${CITUS_PORT:-5439}:5432" in coordinator["ports"]
    assert coordinator["depends_on"]["citus-worker-1"]["condition"] == "service_healthy"
    assert coordinator["depends_on"]["citus-worker-2"]["condition"] == "service_healthy"
    assert "./initdb-citus:/docker-entrypoint-initdb.d:ro" in coordinator["volumes"]
    assert (
        "./initdb-citus-worker:/docker-entrypoint-initdb.d:ro"
        in services["citus-worker-1"]["volumes"]
    )
    assert (
        "./initdb-citus-worker:/docker-entrypoint-initdb.d:ro"
        in services["citus-worker-2"]["volumes"]
    )
    assert "pgfound-citus-coordinator-data" in compose["volumes"]
    assert "pgfound-citus-worker-1-data" in compose["volumes"]
    assert "pgfound-citus-worker-2-data" in compose["volumes"]


def test_citus_initdb_registers_workers() -> None:
    init_sql = Path("docker/initdb-citus/00-citus-cluster.sql").read_text()

    assert "CREATE EXTENSION IF NOT EXISTS citus;" in init_sql
    assert "citus_add_node('citus-worker-1', 5432)" in init_sql
    assert "citus_add_node('citus-worker-2', 5432)" in init_sql


def test_pgpartman_profile_uses_custom_image() -> None:
    compose = load_compose()
    service = compose["services"]["pgpartman"]

    assert service["build"]["context"] == "./pg-with-partman"
    assert service["profiles"] == ["pgpartman"]
    assert "${PGPARTMAN_PORT:-5440}:5432" in service["ports"]
    assert "pgfound-pgpartman-data" in compose["volumes"]
    assert "pg_partman_bgw" in ",".join(service["command"])


def test_pgpartman_initdb_enables_extension() -> None:
    init_sql = Path("docker/initdb-pgpartman/00-pg-partman.sql").read_text()

    assert "CREATE EXTENSION IF NOT EXISTS pg_partman" in init_sql

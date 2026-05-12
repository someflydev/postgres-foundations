from pathlib import Path

import yaml

COMPOSE_FILE = Path("docker/docker-compose.yml")


def load_compose() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text())


def test_timescale_profile_references_pinned_image() -> None:
    compose = load_compose()
    service = compose["services"]["timescale"]

    assert service["image"] == "timescale/timescaledb:2.15.3-pg16"
    assert service["profiles"] == ["timescale"]
    assert "${TIMESCALE_PORT:-5438}:5432" in service["ports"]
    assert "./initdb-timescale:/docker-entrypoint-initdb.d:ro" in service["volumes"]
    assert "pgfound-timescale-data" in compose["volumes"]


def test_timescale_initdb_enables_extension() -> None:
    init_sql = Path("docker/initdb-timescale/00-timescaledb.sql").read_text()

    assert "CREATE EXTENSION IF NOT EXISTS timescaledb;" in init_sql

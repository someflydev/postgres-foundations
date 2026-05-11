from pathlib import Path

import yaml

COMPOSE_FILE = Path("docker/docker-compose.yml")


def load_compose() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text())


def test_pooling_profile_references_pg() -> None:
    compose = load_compose()
    pgbouncer = compose["services"]["pgbouncer"]

    assert pgbouncer["profiles"] == ["pooling"]
    assert pgbouncer["depends_on"]["pg"]["condition"] == "service_healthy"
    assert "${PGBOUNCER_PORT:-6432}:5432" in pgbouncer["ports"]
    assert "pg_isready -h 127.0.0.1 -p 5432" in " ".join(pgbouncer["healthcheck"]["test"])

    ini = Path("docker/pgbouncer/pgbouncer.ini").read_text(encoding="utf-8")
    assert "host=pg" in ini
    assert "pool_mode = transaction" in ini


def test_hba_overlay_profile_mounts_overlay_file() -> None:
    compose = load_compose()
    service = compose["services"]["pg-hba-overlay"]

    assert service["profiles"] == ["hba_overlay"]
    assert "./hba_overlay/pg_hba.conf:/etc/postgresql/pg_hba_overlay.conf:ro" in service["volumes"]
    assert "hba_file=/etc/postgresql/pg_hba_overlay.conf" in service["command"]

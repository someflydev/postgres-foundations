from pathlib import Path

import yaml

COMPOSE_FILE = Path("docker/docker-compose.yml")


def load_compose() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text())


def test_pg_uses_pinned_postgres_16_image() -> None:
    compose = load_compose()

    assert compose["services"]["pg"]["image"] == "postgres:16"


def test_pg_has_healthcheck() -> None:
    compose = load_compose()

    healthcheck = compose["services"]["pg"].get("healthcheck")

    assert healthcheck is not None
    assert "pg_isready -U pgfound -d pgfound" in healthcheck["test"]


def test_pg_mounts_initdb_read_only() -> None:
    compose = load_compose()

    volumes = compose["services"]["pg"]["volumes"]

    assert "./initdb:/docker-entrypoint-initdb.d:ro" in volumes


def test_sandbox_is_gated_by_profile() -> None:
    compose = load_compose()

    sandbox = compose["services"]["pg-sandbox"]

    assert sandbox["image"] == "postgres:16"
    assert sandbox["profiles"] == ["sandbox"]


def test_replication_lab_is_gated_by_profile() -> None:
    compose = load_compose()

    replica = compose["services"]["pg-replica"]

    assert replica["image"] == "postgres:16"
    assert replica["profiles"] == ["replication"]
    assert "${POSTGRES_REPLICA_PORT:-5435}:5432" in replica["ports"]
    assert "wal_level=logical" in replica["command"]
    assert "wal_level=logical" in compose["services"]["pg"]["command"]

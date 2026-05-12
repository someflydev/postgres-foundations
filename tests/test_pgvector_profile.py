from pathlib import Path

import yaml

COMPOSE_FILE = Path("docker/docker-compose.yml")


def load_compose() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text())


def test_pgvector_profile_references_pinned_image() -> None:
    compose = load_compose()
    service = compose["services"]["pgvector"]

    assert service["image"] == "pgvector/pgvector:pg16"
    assert service["profiles"] == ["pgvector"]
    assert "${PGVECTOR_PORT:-5437}:5432" in service["ports"]
    assert "./initdb:/docker-entrypoint-initdb.d:ro" in service["volumes"]
    assert "pgfound-pgvector-data" in compose["volumes"]

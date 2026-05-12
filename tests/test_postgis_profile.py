from pathlib import Path

import yaml

COMPOSE_FILE = Path("docker/docker-compose.yml")


def load_compose() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text())


def test_postgis_profile_references_pinned_image() -> None:
    compose = load_compose()
    service = compose["services"]["postgis"]

    assert service["image"] == "postgis/postgis:16-3.4"
    assert service["profiles"] == ["postgis"]
    assert "${POSTGIS_PORT:-5436}:5432" in service["ports"]
    assert "./initdb:/docker-entrypoint-initdb.d:ro" in service["volumes"]
    assert "pgfound-postgis-data" in compose["volumes"]

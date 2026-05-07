"""Small environment-backed platform config."""

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    postgres_user: str = "pgfound"
    postgres_password: str = "pgfound"
    postgres_db: str = "pgfound"
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 55433
    postgres_sandbox_port: int = 55434


def _read_toml(path: Path | None) -> dict[str, object]:
    if path is None or not path.exists():
        return {}
    with path.open("rb") as config_file:
        parsed = tomllib.load(config_file)
    section = parsed.get("pgfound", parsed)
    return section if isinstance(section, dict) else {}


def _env_or_toml(name: str, toml: dict[str, object], default: object) -> object:
    return os.environ.get(name, toml.get(name.lower(), default))


def load_config(path: Path | None = None) -> Config:
    """Load config from optional TOML plus environment overrides."""
    toml = _read_toml(path)
    return Config(
        postgres_user=str(_env_or_toml("POSTGRES_USER", toml, Config.postgres_user)),
        postgres_password=str(_env_or_toml("POSTGRES_PASSWORD", toml, Config.postgres_password)),
        postgres_db=str(_env_or_toml("POSTGRES_DB", toml, Config.postgres_db)),
        postgres_host=str(_env_or_toml("POSTGRES_HOST", toml, Config.postgres_host)),
        postgres_port=int(_env_or_toml("POSTGRES_PORT", toml, Config.postgres_port)),
        postgres_sandbox_port=int(
            _env_or_toml("POSTGRES_SANDBOX_PORT", toml, Config.postgres_sandbox_port)
        ),
    )

"""Thin wrappers over docker compose for the PostgreSQL lab."""

import json
import logging
import os
import subprocess

from pgfound import paths
from pgfound.lab.psql import build_argv

LOGGER = logging.getLogger(__name__)


def _compose_cmd(*args: str, profile: str | None = None) -> list[str]:
    cmd = ["docker", "compose"]
    if profile:
        cmd.extend(["--profile", profile])
    cmd.extend(args)
    return cmd


def run_compose(
    *args: str, profile: str | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    cmd = _compose_cmd(*args, profile=profile)
    LOGGER.debug("running command: %s", " ".join(cmd))
    return subprocess.run(cmd, cwd=paths.DOCKER_DIR, check=check, text=True)


def up(detach: bool = True, profile: str | None = None) -> subprocess.CompletedProcess[str]:
    args = ["up"]
    if detach:
        args.append("--detach")
    return run_compose(*args, profile=profile)


def down(volumes: bool = False) -> subprocess.CompletedProcess[str]:
    args = ["down"]
    if volumes:
        args.append("--volumes")
    return run_compose(*args)


def ps_json() -> list[dict]:
    cmd = _compose_cmd("ps", "--format", "json")
    LOGGER.debug("running command: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=paths.DOCKER_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    if not output:
        return []
    if output.startswith("["):
        parsed = json.loads(output)
        return parsed if isinstance(parsed, list) else [parsed]
    return [json.loads(line) for line in output.splitlines() if line.strip()]


def logs(service: str | None = None, follow: bool = False) -> subprocess.CompletedProcess[str]:
    args = ["logs"]
    if follow:
        args.append("--follow")
    if service:
        args.append(service)
    return run_compose(*args)


def exec_psql_interactive(user: str, db: str) -> None:
    argv = build_argv(user=user, db=db)
    LOGGER.debug("execvp command: %s", " ".join(argv))
    os.chdir(paths.DOCKER_DIR)
    os.execvp(argv[0], argv)

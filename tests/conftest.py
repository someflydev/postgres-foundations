import shutil
import subprocess

import pytest

from pgfound.content import seed


@pytest.fixture(scope="session")
def lab_available() -> bool:
    """Return True when the default PostgreSQL lab appears reachable."""
    if shutil.which("docker") is None:
        return False
    try:
        subprocess.run(
            ["docker", "info"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    try:
        import psycopg

        with psycopg.connect(seed.database_url(), connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() == (1,)
    except Exception:
        return False


@pytest.fixture(scope="session")
def sandbox_lab_available() -> bool:
    """Return True when the sandbox lab profile appears reachable."""
    if shutil.which("docker") is None:
        return False
    try:
        import psycopg

        with psycopg.connect(seed.sandbox_database_url(), connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() == (1,)
    except Exception:
        return False

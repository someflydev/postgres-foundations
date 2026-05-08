import subprocess
import sys

from pgfound import paths


def test_generators_are_deterministic() -> None:
    generators = sorted((paths.SEED_DATA_DIR / "packs").glob("*/generators/*.py"))
    assert generators

    for generator in generators:
        first = subprocess.run(
            [sys.executable, str(generator)],
            check=True,
            capture_output=True,
        )
        second = subprocess.run(
            [sys.executable, str(generator)],
            check=True,
            capture_output=True,
        )

        assert first.stdout == second.stdout

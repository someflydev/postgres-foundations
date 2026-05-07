"""Pure psql argv builders for the Docker lab."""


def build_argv(user: str = "pgfound", db: str = "pgfound") -> list[str]:
    """Build the interactive docker compose psql argv."""
    return ["docker", "compose", "exec", "pg", "psql", "-U", user, "-d", db]

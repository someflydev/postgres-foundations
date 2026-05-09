"""Pure psql argv builders for the Docker lab."""


def build_argv(
    user: str = "pgfound",
    db: str = "pgfound",
    *,
    search_path: str | None = None,
) -> list[str]:
    """Build the interactive docker compose psql argv."""
    argv = ["docker", "compose", "exec"]
    if search_path:
        normalized_search_path = search_path.replace(" ", "")
        argv.extend(["-e", f"PGOPTIONS=-c search_path={normalized_search_path}"])
    argv.extend(["pg", "psql", "-U", user, "-d", db])
    return argv

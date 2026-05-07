from pgfound.lab import psql


def test_build_argv_returns_interactive_docker_compose_psql_command() -> None:
    assert psql.build_argv(user="alice", db="training") == [
        "docker",
        "compose",
        "exec",
        "pg",
        "psql",
        "-U",
        "alice",
        "-d",
        "training",
    ]

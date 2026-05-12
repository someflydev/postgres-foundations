import subprocess
from unittest.mock import patch

from click.testing import CliRunner

import pgfound
from pgfound.cli import main


def test_version_prints_package_version() -> None:
    result = CliRunner().invoke(main, ["version"])

    assert result.exit_code == 0
    assert pgfound.__version__ in result.output


def test_doctor_runs_without_real_docker() -> None:
    docker_version = subprocess.CompletedProcess(
        args=["docker", "--version"],
        returncode=0,
        stdout="Docker version 27.0.0\n",
        stderr="",
    )
    compose_config = subprocess.CompletedProcess(
        args=["docker", "compose", "config"],
        returncode=0,
        stdout="name: postgres-foundations\n",
        stderr="",
    )

    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("subprocess.run", side_effect=[docker_version, compose_config]),
    ):
        result = CliRunner().invoke(main, ["doctor"])

    assert result.exit_code == 0
    assert "pgfound doctor" in result.output
    assert "Docker version 27.0.0" in result.output
    assert "Compose profile: postgis" in result.output
    assert "Compose profile: pgvector" in result.output
    assert "Compose profile: citus" in result.output
    assert "Compose profile: pgpartman" in result.output


def test_content_list_lesson_shows_scaffolded_draft() -> None:
    result = CliRunner().invoke(main, ["content", "list", "--kind", "lesson"])

    assert result.exit_code == 0
    assert "first-select" in result.output


def test_stub_commands_exit_zero_with_prompt_numbers() -> None:
    runner = CliRunner()

    cases = [
        (["interview", "start"], "PROMPT_28"),
    ]
    for args, prompt in cases:
        result = runner.invoke(main, args)
        assert result.exit_code == 0
        assert prompt in result.output


def test_review_command_help_surfaces_real_review_engine() -> None:
    runner = CliRunner()

    for args in (
        ["exercise", "review", "--help"],
        ["capstone", "evaluate", "--help"],
        ["review", "run", "--help"],
    ):
        result = runner.invoke(main, args)
        assert result.exit_code == 0
        assert "PROMPT_27" not in result.output


def test_root_help_lists_command_groups() -> None:
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    for command in [
        "capstone",
        "content",
        "decision",
        "doctor",
        "interview",
        "lab",
        "review",
        "version",
    ]:
        assert command in result.output

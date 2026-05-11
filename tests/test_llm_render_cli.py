from click.testing import CliRunner

from pgfound.cli import main


def test_llm_render_cli_writes_prompt(tmp_path) -> None:
    out = tmp_path / "prompt.md"
    result = CliRunner().invoke(
        main,
        [
            "llm",
            "render",
            "critique/query-critique",
            "--context",
            "tests/fixtures/critique-context.json",
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.output
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "first-select-write-query" in text
    assert "Learner SQL" in text


def test_llm_list_cli_shows_templates() -> None:
    result = CliRunner().invoke(main, ["llm", "list"])

    assert result.exit_code == 0, result.output
    assert "critique/query-critique" in result.output

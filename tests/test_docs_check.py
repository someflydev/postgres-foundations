from pathlib import Path

from click.testing import CliRunner

from pgfound import docs as docs_checker
from pgfound.cli import main


def test_docs_check_fixture_reports_broken_links(tmp_path: Path) -> None:
    (tmp_path / "index.md").write_text(
        "# Index\n\n[Missing](missing.md)\n",
        encoding="utf-8",
    )

    result = docs_checker.validate_markdown_links(tmp_path)

    assert result.errors == (f"{tmp_path / 'index.md'}: broken link target missing.md",)


def test_docs_check_cli_passes_for_repo_docs() -> None:
    result = CliRunner().invoke(main, ["docs", "check"])

    assert result.exit_code == 0, result.output
    assert "docs check passed" in result.output

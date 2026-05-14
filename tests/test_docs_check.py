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


def test_public_docs_check_validates_contributing_links(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# README\n\n[Docs](docs/)\n", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n[Missing](missing.md)\n",
        encoding="utf-8",
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")

    result = docs_checker.validate_public_docs(tmp_path)

    assert result.errors == ("CONTRIBUTING.md: broken link target missing.md",)


def test_docs_check_cli_passes_for_repo_docs() -> None:
    result = CliRunner().invoke(main, ["docs", "check"])

    assert result.exit_code == 0, result.output
    assert "docs check passed" in result.output

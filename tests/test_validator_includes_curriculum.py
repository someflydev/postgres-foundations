from click.testing import CliRunner

from pgfound.cli import main


def test_content_validate_includes_curriculum_map() -> None:
    result = CliRunner().invoke(main, ["content", "validate"])

    assert result.exit_code == 0
    assert "curriculum" in result.output
    assert "PASS: checked 1 file(s)" in result.output

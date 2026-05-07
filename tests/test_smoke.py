from click.testing import CliRunner

import pgfound
from pgfound.cli import main


def test_package_and_cli_smoke() -> None:
    assert pgfound.__version__ == "0.0.1"

    result = CliRunner().invoke(main)

    assert result.exit_code == 0
    assert "pgfound CLI — not yet implemented" in result.output

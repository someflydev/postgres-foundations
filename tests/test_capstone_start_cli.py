import shutil

from click.testing import CliRunner

from pgfound import paths
from pgfound.cli import main


def test_capstone_start_copies_starter_and_prints_brief() -> None:
    capstone_id = "01-multi-tenant-saas-crm"
    shutil.rmtree(paths.TMP_DIR / "capstone-work" / capstone_id, ignore_errors=True)
    progress_path = paths.TMP_DIR / "progress" / "capstones" / f"{capstone_id}.json"
    progress_path.unlink(missing_ok=True)

    result = CliRunner().invoke(main, ["capstone", "start", capstone_id])

    assert result.exit_code == 0
    assert "Produce a complete PostgreSQL 16 design" in result.output
    assert (paths.TMP_DIR / "capstone-work" / capstone_id / "schema-skeleton.sql").is_file()
    assert progress_path.is_file()

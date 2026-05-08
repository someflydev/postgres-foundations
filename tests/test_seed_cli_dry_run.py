from click.testing import CliRunner

from pgfound import paths
from pgfound.cli import main

DOMAINS = [
    "ecommerce",
    "scheduling",
    "saas_multi_tenant",
    "event_heavy_ops",
    "document_search",
    "modernization_bridge",
]


def test_seed_cli_dry_run_lists_phase_files_in_order() -> None:
    runner = CliRunner()

    for domain in DOMAINS:
        result = runner.invoke(main, ["content", "seed", domain, "--dry-run"])

        assert result.exit_code == 0, result.output
        phase_01 = paths.SEED_DATA_DIR / "packs" / domain / "phases" / "phase-01.sql"
        phase_02 = paths.SEED_DATA_DIR / "packs" / domain / "phases" / "phase-02.sql"
        expected_01 = str(phase_01.relative_to(paths.REPO_ROOT))
        expected_02 = str(phase_02.relative_to(paths.REPO_ROOT))
        assert expected_01 in result.output
        assert expected_02 in result.output
        assert result.output.index(expected_01) < result.output.index(expected_02)


def test_seed_cli_dry_run_respects_phase_limit() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["content", "seed", "ecommerce", "--phase", "1", "--dry-run"])

    assert result.exit_code == 0, result.output
    assert "seed-data/packs/ecommerce/phases/phase-01.sql" in result.output
    assert "seed-data/packs/ecommerce/phases/phase-02.sql" not in result.output

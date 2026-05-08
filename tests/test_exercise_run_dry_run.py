from click.testing import CliRunner

from pgfound.cli import main


def test_exercise_run_dry_run_prints_prompt_and_seed_plan() -> None:
    result = CliRunner().invoke(
        main,
        ["exercise", "run", "first-select-write-query", "--dry-run"],
    )

    assert result.exit_code == 0, result.output
    assert "Exercise: first-select-write-query" in result.output
    assert "Seed pack: scheduling phase 1" in result.output
    assert "seed-data/packs/scheduling/phases/phase-01.sql" in result.output
    assert "Success criteria:" in result.output
    assert "DRY RUN: would use 1 seed SQL file(s)" in result.output

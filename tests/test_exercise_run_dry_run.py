from click.testing import CliRunner

from pgfound import exercise as exercise_runner
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


def test_exercise_run_dry_run_prints_phase2_seed_plan() -> None:
    result = CliRunner().invoke(
        main,
        ["exercise", "run", "inner-join-level-a-1", "--dry-run"],
    )

    assert result.exit_code == 0, result.output
    assert "Exercise: inner-join-level-a-1" in result.output
    assert "Seed pack: ecommerce phase 2" in result.output
    assert "seed-data/packs/ecommerce/phases/phase-01.sql" in result.output
    assert "seed-data/packs/ecommerce/phases/phase-02.sql" in result.output
    assert "DRY RUN: would use 2 seed SQL file(s)" in result.output


def test_output_comparison_normalization_modes() -> None:
    rows = ['["b"]', '["a"]', '["a"]']

    assert exercise_runner._normalize_rows(rows, comparison="ordered") == rows
    assert exercise_runner._normalize_rows(rows, comparison="unordered") == ['["a"]', '["b"]']
    assert exercise_runner._normalize_rows(rows, comparison="multiset") == [
        '["a"]',
        '["a"]',
        '["b"]',
    ]

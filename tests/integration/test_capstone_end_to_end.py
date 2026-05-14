from __future__ import annotations

import shutil

import pytest
from click.testing import CliRunner
from helpers import ALL_CAPSTONE_IDS

from pgfound import paths, progress
from pgfound.cli import main
from pgfound.content import seed
from pgfound.review import engine
from pgfound.review.models import EvaluationContext, EvaluationRequest


def test_capstone_start_and_reference_auto_evaluation(monkeypatch, tmp_path) -> None:
    work_root = paths.REPO_ROOT / "tmp" / f"integration-capstone-start-{tmp_path.name}"
    work_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(progress.paths, "TMP_DIR", work_root)
    runner = CliRunner()

    for capstone_id in ALL_CAPSTONE_IDS:
        started = runner.invoke(main, ["capstone", "start", capstone_id])
        assert started.exit_code == 0, started.output
        assert (work_root / "capstone-work" / capstone_id).is_dir()

        result = engine.evaluate(
            EvaluationRequest(
                target_id=capstone_id,
                artifact_path=paths.CAPSTONES_DIR / capstone_id / "reference",
                context=EvaluationContext(repo_root=paths.REPO_ROOT),
                target_kind="capstone",
            )
        )
        assert result.overall_score >= 0.85, capstone_id


@pytest.mark.docker
def test_capstone_reference_full_evaluation_with_sandbox_lab(
    sandbox_lab_available: bool, tmp_path
) -> None:
    if not sandbox_lab_available:
        pytest.skip("sandbox PostgreSQL lab profile is not reachable")

    for capstone_id in ALL_CAPSTONE_IDS:
        submission = tmp_path / capstone_id
        shutil.copytree(paths.CAPSTONES_DIR / capstone_id / "reference", submission)
        result = engine.evaluate(
            EvaluationRequest(
                target_id=capstone_id,
                artifact_path=submission,
                context=EvaluationContext(
                    repo_root=paths.REPO_ROOT,
                    db_url=seed.sandbox_database_url(),
                ),
                mode="full",
                target_kind="capstone",
            )
        )
        assert result.overall_score >= 0.85, capstone_id

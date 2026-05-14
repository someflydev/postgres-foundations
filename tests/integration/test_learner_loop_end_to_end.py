from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from pgfound import progress
from pgfound.cli import main
from pgfound.progress.models import LearnerProfile


def _attempt(
    exercise_id: str,
    result: str,
    completed_at: str,
    scores: dict[str, int] | None = None,
) -> dict:
    payload = {
        "started_at": completed_at,
        "completed_at": completed_at,
        "check_result": result,
        "self_assessment": "integration smoke",
    }
    if scores:
        payload["rubric_scores"] = scores
    return payload


def test_learner_progress_remediation_and_next_compose_real_content(
    monkeypatch, tmp_path: Path
) -> None:
    progress_root = tmp_path / "progress"
    tmp_root = progress.paths.REPO_ROOT / "tmp" / "integration-learner-loop"
    monkeypatch.setattr(progress.paths, "TMP_DIR", tmp_root)
    monkeypatch.setattr(progress.store, "progress_root", lambda: progress_root)

    progress.store.write_profile(
        LearnerProfile(
            name="integration learner",
            started_at="2026-05-13T00:00:00+00:00",
            goals=("integration",),
        )
    )
    progress.store.write_exercise_progress(
        "first-select-repair-silent-wrong",
        [_attempt("first-select-repair-silent-wrong", "correct", "2026-05-13T00:01:00+00:00")],
    )
    progress.store.write_exercise_progress(
        "check-constraints-level-c-3",
        [
            _attempt(
                "check-constraints-level-c-3",
                "incorrect",
                "2026-05-13T00:02:00+00:00",
                {"constraints": 1},
            )
        ],
    )
    progress.store.write_exercise_progress(
        "what-lateral-unlocks-level-d-1",
        [_attempt("what-lateral-unlocks-level-d-1", "passed", "2026-05-13T00:03:00+00:00")],
    )
    progress.store.write_exercise_progress(
        "covering-indexes-level-c-1",
        [
            _attempt(
                "covering-indexes-level-c-1",
                "failed",
                "2026-05-13T00:04:00+00:00",
                {"index choice": 1},
            )
        ],
    )

    runner = CliRunner()
    show = runner.invoke(main, ["progress", "export", "--format", "json"])
    assert show.exit_code == 0, show.output
    modules = {item["module_id"]: item for item in json.loads(show.output)["modules"]}
    assert modules["phase-01"]["status"] == "in-progress"
    assert modules["phase-03"]["status"] == "in-progress"
    assert modules["phase-05"]["status"] == "in-progress"
    assert modules["phase-07"]["status"] == "in-progress"

    remediation = runner.invoke(main, ["remediate", "--module", "phase-03", "--scope", "all"])
    assert remediation.exit_code == 0, remediation.output
    assert "constraints" in remediation.output
    remediation_pack = next((tmp_root / "remediation").glob("*.md"))
    assert "Level D" in remediation_pack.read_text(encoding="utf-8")

    next_action = runner.invoke(main, ["next"])
    assert next_action.exit_code == 0, next_action.output
    assert "pgfound remediate" in next_action.output
    assert "constraints" in next_action.output

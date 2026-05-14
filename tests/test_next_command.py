from click.testing import CliRunner

from pgfound.cli import main
from pgfound.progress.models import ExerciseAttempt
from pgfound.progress.store import ProgressSnapshot


def test_next_command_is_deterministic_for_weak_recent_attempt(monkeypatch) -> None:
    snapshot = ProgressSnapshot(
        profile=None,
        exercise_attempts=(
            ExerciseAttempt(
                exercise_id="x",
                started_at="2026-05-13T00:00:00+00:00",
                rubric_scores={"constraints": 1},
            ),
        ),
        capstone_attempts=(),
        interview_attempts=(),
    )
    monkeypatch.setattr("pgfound.progress.store.load_snapshot", lambda: snapshot)

    result = CliRunner().invoke(main, ["next"])

    assert result.exit_code == 0
    assert "pgfound remediate" in result.output
    assert "constraints" in result.output

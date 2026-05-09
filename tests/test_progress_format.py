import json
from pathlib import Path

from pgfound import progress


def test_progress_record_round_trip(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(progress.paths, "REPO_ROOT", tmp_path)

    path = progress.append_exercise_attempt(
        "first-select-write-query",
        started_at="2026-04-23T14:00:00-07:00",
        completed_at="2026-04-23T14:22:00-07:00",
        self_assessment="correct",
        check_result="correct",
        notes="small WHERE clause repair",
    )

    assert path == tmp_path / "tmp" / "progress" / "exercises" / "first-select-write-query.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == {
        "exercise_id": "first-select-write-query",
        "attempts": [
            {
                "started_at": "2026-04-23T14:00:00-07:00",
                "completed_at": "2026-04-23T14:22:00-07:00",
                "self_assessment": "correct",
                "check_result": "correct",
                "notes": "small WHERE clause repair",
            }
        ],
    }

    summary = progress.summarize()
    assert summary.exercise_files == 1
    assert summary.exercise_attempts == 1

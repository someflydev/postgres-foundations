import json
from pathlib import Path

import pytest

from pgfound import progress
from pgfound.progress.models import LearnerProfile


def test_progress_profile_uses_atomic_tmp_rename(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(progress.paths, "REPO_ROOT", tmp_path)

    path = progress.store.write_profile(
        LearnerProfile(name="test", started_at="2026-05-13T00:00:00+00:00", goals=("review",))
    )

    assert path == tmp_path / "tmp" / "progress" / "profile.json"
    assert not (path.parent / "profile.json.tmp").exists()
    assert json.loads(path.read_text(encoding="utf-8"))["name"] == "test"


def test_progress_store_rejects_invalid_attempt_schema(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(progress.paths, "REPO_ROOT", tmp_path)
    path = progress.exercise_progress_path("bad")
    path.parent.mkdir(parents=True)
    path.write_text('{"exercise_id": "bad", "attempts": {}}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="attempts must be a list"):
        progress.read_exercise_progress(path)

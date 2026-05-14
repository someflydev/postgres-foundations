from pathlib import Path

from pgfound import progress
from pgfound.progress import derive
from pgfound.progress.models import ExerciseAttempt
from pgfound.progress.store import ProgressSnapshot


def test_remediation_recommends_low_dimension_pack(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(progress.paths, "TMP_DIR", tmp_path / "tmp")
    monkeypatch.setattr(
        derive,
        "load_lesson_meta",
        lambda: {
            "joins": derive.LessonMeta(
                id="joins",
                module_id="phase-02",
                cluster_id="joining-two-tables",
                title="Joins",
                exercise_ids=("joins-level-d-1",),
                path=tmp_path,
            )
        },
    )
    monkeypatch.setattr(
        derive,
        "load_exercise_meta",
        lambda: {
            "joins-level-d-1": derive.ExerciseMeta(
                id="joins-level-d-1",
                lesson_id="joins",
                level="D",
                module_id="phase-02",
                path=tmp_path,
            )
        },
    )
    monkeypatch.setattr(derive, "all_module_ids", lambda: ["phase-02"])

    snapshot = ProgressSnapshot(
        profile=None,
        exercise_attempts=(
            ExerciseAttempt(
                exercise_id="joins-level-c-1",
                started_at="2026-05-13T00:00:00+00:00",
                rubric_scores={"join grain": 1},
            ),
        ),
        capstone_attempts=(),
        interview_attempts=(),
    )

    pack = progress.remediation.build_remediation_pack(snapshot, module_id="phase-02")

    assert pack.path.is_file()
    assert pack.weaknesses[0] == "join grain"
    assert "skipped Level D exit evidence" in pack.weaknesses
    assert pack.exercises == ("joins-level-d-1",)
    assert "Failure Lab Prompt" in pack.path.read_text(encoding="utf-8")


def test_remediation_uses_failed_comparator_attempt_without_rubric(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(progress.paths, "TMP_DIR", tmp_path / "tmp")
    monkeypatch.setattr(
        derive,
        "load_lesson_meta",
        lambda: {
            "constraints": derive.LessonMeta(
                id="constraints",
                module_id="phase-03",
                cluster_id="constraints-as-truth",
                title="Constraints",
                exercise_ids=("constraints-level-d-1",),
                path=tmp_path,
            )
        },
    )
    monkeypatch.setattr(
        derive,
        "load_exercise_meta",
        lambda: {
            "constraints-level-c-1": derive.ExerciseMeta(
                id="constraints-level-c-1",
                lesson_id="constraints",
                level="C",
                module_id="phase-03",
                path=tmp_path,
            ),
            "constraints-level-d-1": derive.ExerciseMeta(
                id="constraints-level-d-1",
                lesson_id="constraints",
                level="D",
                module_id="phase-03",
                path=tmp_path,
            ),
        },
    )
    monkeypatch.setattr(derive, "all_module_ids", lambda: ["phase-03"])
    snapshot = ProgressSnapshot(
        profile=None,
        exercise_attempts=(
            ExerciseAttempt(
                exercise_id="constraints-level-c-1",
                started_at="2026-05-13T00:00:00+00:00",
                check_result="incorrect",
            ),
        ),
        capstone_attempts=(),
        interview_attempts=(),
    )

    pack = progress.remediation.build_remediation_pack(snapshot, module_id="phase-03")

    assert "constraints evidence" in pack.weaknesses
    assert "skipped Level D exit evidence" in pack.weaknesses

from pgfound.progress import derive
from pgfound.progress.models import ExerciseAttempt


def test_module_progress_requires_level_d_per_cluster(monkeypatch) -> None:
    monkeypatch.setattr(
        derive,
        "load_exercise_meta",
        lambda: {
            "lesson-a-level-d-1": derive.ExerciseMeta(
                id="lesson-a-level-d-1",
                lesson_id="lesson-a",
                level="D",
                module_id="phase-01",
                path=derive.paths.REPO_ROOT,
            ),
            "lesson-b-level-d-1": derive.ExerciseMeta(
                id="lesson-b-level-d-1",
                lesson_id="lesson-b",
                level="D",
                module_id="phase-01",
                path=derive.paths.REPO_ROOT,
            ),
        },
    )
    monkeypatch.setattr(
        derive,
        "load_lesson_meta",
        lambda: {
            "lesson-a": derive.LessonMeta(
                id="lesson-a",
                module_id="phase-01",
                cluster_id="cluster-one",
                title="Lesson A",
                exercise_ids=("lesson-a-level-d-1",),
                path=derive.paths.REPO_ROOT,
            ),
            "lesson-b": derive.LessonMeta(
                id="lesson-b",
                module_id="phase-01",
                cluster_id="cluster-one",
                title="Lesson B",
                exercise_ids=("lesson-b-level-d-1",),
                path=derive.paths.REPO_ROOT,
            ),
        },
    )
    monkeypatch.setattr(derive, "all_module_ids", lambda: ["phase-01"])

    progress = derive.compute_module_progress(
        (
            ExerciseAttempt(
                exercise_id="lesson-a-level-d-1",
                started_at="2026-05-13T00:00:00+00:00",
                completed_at="2026-05-13T00:10:00+00:00",
                check_result="correct",
            ),
        )
    )
    assert progress["phase-01"].status == "in-progress"
    assert progress["phase-01"].evidence == ()

    progress = derive.compute_module_progress(
        (
            ExerciseAttempt(
                exercise_id="lesson-a-level-d-1",
                started_at="2026-05-13T00:00:00+00:00",
                completed_at="2026-05-13T00:10:00+00:00",
                check_result="correct",
            ),
            ExerciseAttempt(
                exercise_id="lesson-b-level-d-1",
                started_at="2026-05-13T00:20:00+00:00",
                completed_at="2026-05-13T00:30:00+00:00",
                rubric_scores={"correctness": 3},
            ),
        )
    )
    assert progress["phase-01"].status == "met"
    assert progress["phase-01"].evidence == ("cluster-one: lesson-b-level-d-1",)

"""Remediation and next-step planning."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pgfound import paths
from pgfound.llm import templates as llm_templates
from pgfound.progress import derive
from pgfound.progress.models import ExerciseAttempt, ModuleProgress
from pgfound.progress.store import ProgressSnapshot


@dataclass(frozen=True)
class RemediationPack:
    path: Path
    module_id: str | None
    weaknesses: tuple[str, ...]
    lessons: tuple[str, ...]
    exercises: tuple[str, ...]
    failure_lab_prompt: str


@dataclass(frozen=True)
class NextAction:
    action: str
    rationale: str


def build_remediation_pack(
    snapshot: ProgressSnapshot, *, module_id: str | None = None, scope: str = "recent"
) -> RemediationPack:
    attempts = list(snapshot.exercise_attempts)
    if scope == "recent":
        attempts = sorted(attempts, key=lambda item: item.completed_at or item.started_at)[-10:]
    progress = derive.compute_module_progress(tuple(snapshot.exercise_attempts))
    target_module = module_id or _first_unmet_module(progress)
    lessons = _recommended_lessons(target_module, limit=4)
    exercises = _recommended_exercises(target_module, tuple(snapshot.exercise_attempts), limit=6)
    weaknesses = _weaknesses(attempts, target_module=target_module, skipped_exercises=exercises)
    concept = weaknesses[0]
    failure_prompt = llm_templates.render_template(
        "remediation/failure-lab-generator",
        {
            "concept_slug": concept.lower().replace(" ", "-"),
            "common_mistake": f"Repeated low score or incomplete evidence for {concept}.",
            "domain_context": target_module or "current PostgreSQL foundations module",
            "allowed_concepts": [concept],
            "not_yet_allowed_concepts": [],
            "learner_review_report": _attempt_summary(attempts),
        },
    )
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = paths.TMP_DIR / "remediation" / f"{timestamp}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    sections = [
        "# Remediation Pack",
        "",
        f"Module: {target_module or 'current'}",
        "",
        "## Weaknesses",
        *[f"- {item}" for item in weaknesses],
        "",
        "## Re-read",
        *[f"- {item}" for item in lessons],
        "",
        "## Complete",
        *[f"- {item}" for item in exercises],
        "",
        "## Failure Lab Prompt",
        failure_prompt.rstrip(),
    ]
    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return RemediationPack(
        path=path,
        module_id=target_module,
        weaknesses=weaknesses,
        lessons=lessons,
        exercises=exercises,
        failure_lab_prompt=failure_prompt,
    )


def recommend_next(snapshot: ProgressSnapshot) -> NextAction:
    progress = derive.compute_module_progress(snapshot.exercise_attempts)
    low_dimensions = _weak_dimensions(snapshot.exercise_attempts)
    if low_dimensions:
        return NextAction(
            action="Run `pgfound remediate`",
            rationale=f"Recent attempts show weak evidence for {low_dimensions[0]}.",
        )
    target_module = _first_unmet_module(progress)
    if target_module:
        exercises = _recommended_exercises(target_module, snapshot.exercise_attempts, limit=1)
        if exercises:
            return NextAction(
                action=f"Complete `{exercises[0]}`",
                rationale=f"{target_module} still has unmet exit competency evidence.",
            )
        return NextAction(
            action=f"Move into `{target_module}`",
            rationale="It is the next module without completed exit evidence.",
        )
    if not snapshot.interview_attempts:
        return NextAction(
            action="Run `pgfound interview start --scenario senior-backend-saas-rls`",
            rationale="The core module evidence is complete enough to practice oral defense.",
        )
    return NextAction(
        action="Start or evaluate a capstone",
        rationale="Module evidence is in good shape; synthesis work is the next useful signal.",
    )


def _weak_dimensions(
    attempts: tuple[ExerciseAttempt, ...] | list[ExerciseAttempt],
) -> tuple[str, ...]:
    totals: Counter[str] = Counter()
    counts: Counter[str] = Counter()
    for attempt in attempts:
        for name, score in attempt.rubric_scores.items():
            if score >= 0:
                totals[name] += score
                counts[name] += 1
    weak = [name for name, count in counts.items() if count >= 1 and totals[name] / count < 3]
    return tuple(sorted(weak, key=lambda name: (totals[name] / counts[name], name))[:3])


def _weaknesses(
    attempts: tuple[ExerciseAttempt, ...] | list[ExerciseAttempt],
    *,
    target_module: str | None,
    skipped_exercises: tuple[str, ...],
) -> tuple[str, ...]:
    weaknesses = list(_weak_dimensions(attempts))
    exercises = derive.load_exercise_meta()
    for attempt in attempts:
        if attempt.rubric_scores:
            continue
        if attempt.check_result.lower() not in {"incorrect", "failed", "fail", "error"}:
            continue
        meta = exercises.get(attempt.exercise_id)
        if meta and (target_module is None or meta.module_id == target_module):
            weaknesses.append(f"{meta.lesson_id or meta.id} evidence")
        else:
            weaknesses.append(f"{attempt.exercise_id} evidence")
    if skipped_exercises:
        weaknesses.append("skipped Level D exit evidence")
    deduped = []
    for weakness in weaknesses:
        if weakness not in deduped:
            deduped.append(weakness)
    return tuple(deduped[:3] or ["exit competency practice"])


def _first_unmet_module(progress: dict[str, ModuleProgress]) -> str | None:
    for module_id, module in progress.items():
        if module.status != "met":
            return module_id
    return None


def _recommended_lessons(module_id: str | None, *, limit: int) -> tuple[str, ...]:
    lessons = [
        lesson
        for lesson in derive.load_lesson_meta().values()
        if module_id is None or lesson.module_id == module_id
    ]
    return tuple(f"{lesson.id} ({lesson.title})" for lesson in lessons[:limit])


def _recommended_exercises(
    module_id: str | None,
    attempts: tuple[ExerciseAttempt, ...] | list[ExerciseAttempt],
    *,
    limit: int,
) -> tuple[str, ...]:
    attempted = {attempt.exercise_id for attempt in attempts}
    exercises = [
        exercise
        for exercise in derive.load_exercise_meta().values()
        if (module_id is None or exercise.module_id == module_id) and exercise.level == "D"
    ]
    skipped = [exercise.id for exercise in exercises if exercise.id not in attempted]
    return tuple((skipped or [exercise.id for exercise in exercises])[:limit])


def _attempt_summary(attempts: list[ExerciseAttempt]) -> str:
    if not attempts:
        return "No learner-specific attempts supplied."
    lines = []
    for attempt in attempts[-5:]:
        lines.append(
            f"- {attempt.exercise_id}: check={attempt.check_result}; scores={attempt.rubric_scores}"
        )
    return "\n".join(lines)

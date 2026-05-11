"""Prompt-template loading for the interview simulator."""

from __future__ import annotations

from dataclasses import dataclass

from pgfound import exercise as exercise_runner
from pgfound import paths
from pgfound.interview.scenario import InterviewScenario, InterviewStage


@dataclass(frozen=True)
class ResolvedPrompt:
    """Prompt text and deterministic follow-ups from a template."""

    text: str
    follow_ups: tuple[str, ...]
    llm_payload: str


def load_prompt(
    scenario: InterviewScenario,
    stage: InterviewStage,
    *,
    learner_context: dict[str, str] | None = None,
) -> ResolvedPrompt:
    """Resolve a stage prompt template with scenario and exercise context."""

    context = {
        "scenario_id": scenario.id,
        "scenario_title": scenario.title,
        "stage_kind": stage.kind,
        "topic": stage.topic or "",
        "exercise_id": stage.exercise_id or "",
        "exercise_prompt": "",
    }
    if stage.exercise_id:
        try:
            record = exercise_runner.find_exercise(stage.exercise_id)
            context["exercise_prompt"] = record.prompt_path.read_text(encoding="utf-8").strip()
        except Exception as exc:
            context["exercise_prompt"] = f"[exercise prompt unavailable: {exc}]"
    if learner_context:
        context.update(learner_context)

    template_text = _template_text(stage)
    body, follow_ups = _split_follow_ups(template_text)
    rendered = body.format_map(_SafeDict(context)).strip()
    rendered_follow_ups = tuple(
        follow_up.format_map(_SafeDict(context)).strip()
        for follow_up in follow_ups
        if follow_up.strip()
    )
    payload = _llm_payload(scenario, stage, rendered, rendered_follow_ups)
    return ResolvedPrompt(text=rendered, follow_ups=rendered_follow_ups, llm_payload=payload)


def _template_text(stage: InterviewStage) -> str:
    if not stage.prompt_template:
        return (
            "Work through the referenced exercise aloud.\n\n"
            "{exercise_prompt}\n\n"
            "## Follow-ups\n"
            "- What correctness risk are you testing for?\n"
            "- What evidence would convince you the fix works?\n"
            "- How would you explain the failure mode to a teammate?\n"
        )
    path = paths.LLM_PROMPTS_DIR / f"{stage.prompt_template}.md"
    if not path.is_file():
        msg = f"prompt template not found: {path.relative_to(paths.REPO_ROOT)}"
        raise ValueError(msg)
    return path.read_text(encoding="utf-8")


def _split_follow_ups(template_text: str) -> tuple[str, tuple[str, ...]]:
    marker = "## Follow-ups"
    if marker not in template_text:
        return template_text, ()
    body, follow_up_block = template_text.split(marker, 1)
    follow_ups = []
    for line in follow_up_block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            follow_ups.append(stripped[2:])
    return body, tuple(follow_ups)


def _llm_payload(
    scenario: InterviewScenario,
    stage: InterviewStage,
    prompt: str,
    follow_ups: tuple[str, ...],
) -> str:
    lines = [
        f"scenario_id: {scenario.id}",
        f"stage_kind: {stage.kind}",
        f"topic: {stage.topic or ''}",
        f"exercise_id: {stage.exercise_id or ''}",
        "",
        "prompt:",
        prompt,
    ]
    if follow_ups:
        lines.extend(["", "follow_up_questions:"])
        lines.extend(f"- {item}" for item in follow_ups)
    return "\n".join(lines).strip()


class _SafeDict(dict[str, str]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"

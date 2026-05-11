"""Prompt-template rendering for the interview simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pgfound import exercise as exercise_runner
from pgfound.interview.scenario import InterviewScenario, InterviewStage
from pgfound.llm import templates as llm_templates


@dataclass(frozen=True)
class ResolvedPrompt:
    """Rendered prompt text and deterministic prompt metadata."""

    text: str
    template_id: str
    llm_payload: str


def persona_template_id(scenario: InterviewScenario) -> str:
    """Choose the interviewer persona template for a scenario."""
    if scenario.id == "architect-decision-engine-review":
        return "interview/personas/adversarial-architect"
    if scenario.id.startswith("mid-level"):
        return "interview/personas/mid-interviewer"
    return "interview/personas/senior-interviewer"


def render_persona(scenario: InterviewScenario) -> ResolvedPrompt:
    """Render the persona template for an interview scenario."""
    template_id = persona_template_id(scenario)
    context = _base_context(scenario)
    rendered = llm_templates.render_template(template_id, context)
    return ResolvedPrompt(text=rendered, template_id=template_id, llm_payload=rendered)


def load_prompt(
    scenario: InterviewScenario,
    stage: InterviewStage,
    *,
    previous_stages: list[dict[str, str]] | None = None,
    latest_response: str = "",
    full_transcript: str = "",
) -> ResolvedPrompt:
    """Render a stage prompt template with scenario, transcript, and exercise context."""

    template_id = stage.prompt_template or "interview/stages/debugging-drill-wrap"
    context = {
        **_base_context(scenario),
        "stage_kind": stage.kind,
        "topic": stage.topic or "",
        "exercise_id": stage.exercise_id or "",
        "exercise_prompt": _exercise_prompt(stage),
        "previous_stages": previous_stages or [],
        "latest_response": latest_response,
        "full_transcript": full_transcript,
    }
    rendered = llm_templates.render_template(template_id, context)
    payload = _llm_payload(scenario, stage, template_id, rendered)
    return ResolvedPrompt(text=rendered, template_id=template_id, llm_payload=payload)


def render_follow_ups(
    scenario: InterviewScenario,
    stage: InterviewStage,
    *,
    stage_transcript: str,
) -> ResolvedPrompt:
    """Render the progressive follow-up generator for a stage transcript."""
    template_id = "interview/follow-up-generator"
    context = {
        **_base_context(scenario),
        "stage_kind": stage.kind,
        "topic": stage.topic or "",
        "stage_transcript": stage_transcript,
    }
    rendered = llm_templates.render_template(template_id, context)
    return ResolvedPrompt(text=rendered, template_id=template_id, llm_payload=rendered)


def _base_context(scenario: InterviewScenario) -> dict[str, Any]:
    return {
        "scenario_id": scenario.id,
        "scenario_title": scenario.title,
        "duration_minutes": scenario.duration_minutes,
        "capability_layers_required": list(scenario.capability_layers_required),
        "rubric_id": scenario.rubric_id,
    }


def _exercise_prompt(stage: InterviewStage) -> str:
    if not stage.exercise_id:
        return ""
    try:
        record = exercise_runner.find_exercise(stage.exercise_id)
        return record.prompt_path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        return f"[exercise prompt unavailable: {exc}]"


def _llm_payload(
    scenario: InterviewScenario,
    stage: InterviewStage,
    template_id: str,
    prompt: str,
) -> str:
    return "\n".join(
        [
            f"scenario_id: {scenario.id}",
            f"stage_kind: {stage.kind}",
            f"template_id: {template_id}",
            f"topic: {stage.topic or ''}",
            f"exercise_id: {stage.exercise_id or ''}",
            "",
            "rendered_prompt:",
            prompt,
        ]
    ).strip()

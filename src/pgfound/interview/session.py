"""Interview session state machine."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

from pgfound import exercise as exercise_runner
from pgfound.interview import prompts, rubric, transcripts
from pgfound.interview.scenario import InterviewScenario

LLM_STUB = "[LLM response intentionally stubbed; rendered provider-neutral prompt captured]"


@dataclass(frozen=True)
class SessionResult:
    """Completed interview session result."""

    transcript_path: Path
    review_summary: str


def run_session(
    scenario: InterviewScenario,
    *,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    learner: str = "local-learner",
    sleep_seconds: float = 0.0,
) -> SessionResult:
    """Run a stubbed interview session and write its transcript."""

    input_stream = stdin or sys.stdin
    output_stream = stdout or sys.stdout
    started_at = _now()
    captured_stages: list[dict[str, str]] = []
    persona_prompt = ""

    print(f"Interview: {scenario.title}", file=output_stream)
    print(f"Scenario: {scenario.id}", file=output_stream)
    for index, stage in enumerate(scenario.stages):
        resolved = prompts.load_prompt(
            scenario,
            stage,
            previous_stages=_previous_stage_context(captured_stages),
        )
        print("", file=output_stream)
        print(f"== Stage: {stage.kind} ({stage.budget_minutes} min) ==", file=output_stream)
        print(resolved.text, file=output_stream)
        _print_timer(stage.budget_minutes, output_stream=output_stream, sleep_seconds=sleep_seconds)
        print("Enter response. End with /next or EOF.", file=output_stream)
        response = _read_response(input_stream)
        notes = _stage_notes(scenario, stage, resolved, response, output_stream=output_stream)
        print(LLM_STUB, file=output_stream)
        captured_stages.append(
            {
                "kind": stage.kind,
                "prompt": resolved.text,
                "learner_response": response,
                "simulator_notes": notes,
            }
        )
        if index == 0:
            persona = prompts.render_persona(scenario)
            persona_prompt = persona.text
            captured_stages[-1]["simulator_notes"] += (
                "\n\nPersona prompt rendered after warmup:\n\n```markdown\n"
                + persona.text.rstrip()
                + "\n```"
            )

    closing = prompts.load_prompt(
        scenario,
        _closing_stage(),
        previous_stages=_previous_stage_context(captured_stages),
        full_transcript=_stage_summary(captured_stages),
    )
    captured_stages.append(
        {
            "kind": "closing_feedback",
            "prompt": closing.text,
            "learner_response": "[closing feedback generated from transcript]",
            "simulator_notes": _closing_notes(closing),
        }
    )

    completed_at = _now()
    path = transcripts.transcript_path(scenario.id)
    transcripts.write_transcript(
        path,
        scenario=scenario,
        started_at=started_at,
        completed_at=completed_at,
        learner=learner,
        persona_prompt=persona_prompt,
        stages=captured_stages,
    )
    result = rubric.evaluate(path)
    summary = rubric.format_summary(result)
    print("", file=output_stream)
    print(f"Transcript: {path}", file=output_stream)
    print(summary, file=output_stream)
    return SessionResult(transcript_path=path, review_summary=summary)


def _read_response(input_stream: TextIO) -> str:
    lines = []
    for line in input_stream:
        if line.rstrip("\n") == "/next":
            break
        lines.append(line.rstrip("\n"))
    return "\n".join(lines).strip()


def _print_timer(budget_minutes: int, *, output_stream: TextIO, sleep_seconds: float) -> None:
    print(f"Timer opened: {budget_minutes} minute(s) remaining.", file=output_stream)
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    print("Timer checkpoint: continue or type /next when ready.", file=output_stream)


def _stage_notes(
    scenario: InterviewScenario,
    stage,
    resolved,
    learner_response: str,
    *,
    output_stream: TextIO,
) -> str:
    lines = [
        f"Rendered prompt template: `{resolved.template_id}`",
        "",
        "What the simulator would send to the LLM:",
        "",
        "### Rendered Prompt",
        "```markdown",
        resolved.text,
        "```",
        "",
        "### LLM Dispatch Payload",
        "```yaml",
        resolved.llm_payload,
        "```",
        "",
        f"Stubbed LLM response: {LLM_STUB}",
    ]
    if stage.kind == "debugging_drill" and stage.exercise_id:
        lines.extend(["", "Debugging drill check:"])
        try:
            record = exercise_runner.find_exercise(stage.exercise_id)
            correct, diff = exercise_runner.check_answer(record)
            result = "correct" if correct else "incorrect"
            lines.append(result)
            if diff:
                lines.append(diff)
            print(f"Exercise check: {result}", file=output_stream)
        except Exception as exc:
            lines.append(f"not run: {exc}")
            print(f"Exercise check not run: {exc}", file=output_stream)
    if stage.kind in {"design_probe", "explainability", "debugging_drill"} and learner_response:
        follow_up = prompts.render_follow_ups(
            scenario,
            stage,
            stage_transcript="\n\n".join(
                [
                    f"Prompt:\n{resolved.text}",
                    f"Learner response:\n{learner_response or '[no response recorded]'}",
                ]
            ),
        )
        print("Follow-up questions:", file=output_stream)
        print(follow_up.text, file=output_stream)
        lines.extend(["", "### Follow-Up Generator Prompt", "```markdown", follow_up.text, "```"])
    return "\n".join(lines).strip()


def _closing_notes(resolved) -> str:
    return "\n".join(
        [
            f"Rendered prompt template: `{resolved.template_id}`",
            "",
            "### Rendered Prompt",
            "```markdown",
            resolved.text,
            "```",
            "",
            f"Stubbed LLM response: {LLM_STUB}",
        ]
    ).strip()


def _closing_stage():
    return type(
        "ClosingStage",
        (),
        {
            "kind": "closing_feedback",
            "budget_minutes": 0,
            "prompt_template": "interview/stages/closing-feedback",
            "topic": "closing_feedback",
            "exercise_id": None,
        },
    )()


def _stage_summary(stages: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for stage in stages:
        lines.extend(
            [
                f"## Stage: {stage['kind']}",
                "### Prompt",
                stage["prompt"],
                "### Learner response",
                stage["learner_response"] or "[no response recorded]",
                "",
            ]
        )
    return "\n".join(lines).strip()


def _previous_stage_context(stages: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "kind": stage["kind"],
            "learner_response": stage["learner_response"] or "[no response recorded]",
        }
        for stage in stages
    ]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

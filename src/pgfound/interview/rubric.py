"""Deterministic interview transcript rubric evaluation."""

from __future__ import annotations

from pathlib import Path

from pgfound.interview import scenario as scenario_loader
from pgfound.interview import transcripts
from pgfound.review import grading
from pgfound.review.models import DimensionScore, EvaluationResult, Finding, Signal


def evaluate(transcript_path: Path) -> EvaluationResult:
    """Evaluate an interview transcript with weak deterministic signals."""

    transcript = transcripts.validate_transcript(transcript_path)
    scenario = scenario_loader.load_scenario(transcript.scenario_id)
    text = transcript.raw_text.lower()
    response_text = "\n\n".join(stage.learner_response for stage in transcript.stages).lower()
    signals = _signals(response_text, text)
    findings = _findings(response_text, transcript_path)
    rubric = grading.load_rubric(scenario.rubric_id)
    dimensions, overall, passed = grading.evaluate_rubric(rubric, signals)
    return EvaluationResult(
        target_id=transcript.scenario_id,
        target_kind="interview",
        rubric_id=str(rubric["id"]),
        dimensions=dimensions,
        overall_score=overall,
        passed=passed,
        findings=tuple(findings),
        signals=tuple(signals),
        report_paths={},
    )


def format_summary(result: EvaluationResult) -> str:
    """Render a compact text score breakdown."""

    lines = [
        f"Interview review: {result.target_id}",
        f"Rubric: {result.rubric_id}",
        f"Overall: {result.overall_score:.2f}",
        f"Passed: {'yes' if result.passed else 'no'}",
        "",
        "Dimensions:",
    ]
    for dimension in result.dimensions:
        lines.append(_dimension_line(dimension))
    if result.findings:
        lines.extend(["", "Findings:"])
        lines.extend(f"- {finding.severity}: {finding.title}" for finding in result.findings)
    return "\n".join(lines)


def _signals(response_text: str, full_text: str) -> list[Signal]:
    words = [word for word in response_text.split() if word.strip()]
    has_because = "because" in response_text or "so that" in response_text
    has_tradeoff = "tradeoff" in response_text or "trade-off" in response_text
    has_later = "not yet" in response_text or "later" in response_text
    has_ops = any(term in response_text for term in ("monitor", "rollback", "migration", "bloat"))
    has_correctness = any(
        term in response_text for term in ("transaction", "constraint", "isolation", "lock")
    )
    has_llm_payload = "what the simulator would send to the llm" in full_text
    return [
        Signal(
            "communication_detail",
            _level_value(len(words), [(180, "strong"), (80, "adequate")]),
            "Counted learner response words.",
        ),
        Signal(
            "decision_justification",
            "strong" if has_because and has_tradeoff else "adequate" if has_because else "weak",
            "Looked for explicit because/tradeoff reasoning.",
        ),
        Signal(
            "operational_awareness",
            "strong" if has_ops and has_later else "adequate" if has_ops or has_later else "weak",
            "Looked for operational and not-yet/later language.",
        ),
        Signal(
            "correctness_language",
            "strong" if has_correctness else "weak",
            "Looked for correctness vocabulary.",
        ),
        Signal(
            "stubbed_llm_logged",
            "present" if has_llm_payload else "missing",
            "Checked simulator notes for the stubbed LLM payload.",
        ),
    ]


def _findings(response_text: str, transcript_path: Path) -> list[Finding]:
    if response_text.strip() and len(response_text.split()) >= 40:
        return []
    return [
        Finding(
            "warning",
            "Learner response is short",
            "Interview signal may be weak because the transcript has little learner explanation.",
            str(transcript_path),
            "Communication",
        )
    ]


def _level_value(count: int, thresholds: list[tuple[int, str]]) -> str:
    for threshold, value in thresholds:
        if count >= threshold:
            return value
    return "weak"


def _dimension_line(dimension: DimensionScore) -> str:
    score = "manual" if dimension.manual_review else f"{dimension.score}/{dimension.max_score}"
    return f"- {dimension.name}: {score} (weight {dimension.weight:.2f})"

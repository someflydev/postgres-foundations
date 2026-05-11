from pathlib import Path
from unittest.mock import patch

from pgfound.review import engine
from pgfound.review.models import EvaluationContext, EvaluationRequest


def test_exercise_review_emits_correctness_findings_for_wrong_answer(tmp_path: Path) -> None:
    answer = tmp_path / "answer.sql"
    answer.write_text("select 1;\n", encoding="utf-8")

    with (
        patch("pgfound.exercise.auto_seed"),
        patch(
            "pgfound.exercise.check_answer_with_timing",
            return_value=(False, "--- expected\n+++ actual", {}),
        ),
    ):
        result = engine.evaluate(
            EvaluationRequest(
                target_id="first-select-write-query",
                artifact_path=answer,
                context=EvaluationContext(repo_root=tmp_path),
                target_kind="exercise",
            )
        )

    assert result.target_kind == "exercise"
    assert result.overall_score < 0.75
    assert ("output_matches_reference", "missing") in {
        (signal.key, signal.value) for signal in result.signals
    }
    assert any(finding.severity == "error" for finding in result.findings)
    assert result.report_paths["markdown"].endswith(".md")

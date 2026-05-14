from __future__ import annotations

from io import StringIO
from unittest.mock import patch

from pgfound import paths
from pgfound.interview import rubric, session, transcripts
from pgfound.interview import scenario as scenario_loader

GOOD_ANSWER_BLOCK = (
    "I would start with the workload and data ownership because the database has to preserve "
    "correctness before optimization. The tradeoff is operational cost, so I would choose the "
    "simplest core PostgreSQL design first, add constraints and transaction checks, monitor query "
    "plans and bloat, and defer extra extensions until the workload shows a real need.\n"
    "/next\n"
)


def test_all_interview_scenarios_produce_reviewable_transcripts(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(transcripts.paths, "TMP_DIR", tmp_path)
    scenario_ids = sorted(path.stem for path in (paths.SCENARIOS_DIR / "interviews").glob("*.yaml"))
    assert len(scenario_ids) == 6

    with patch("pgfound.interview.session.exercise_runner.check_answer", return_value=(True, "")):
        for scenario_id in scenario_ids:
            scenario = scenario_loader.load_scenario(scenario_id)
            stdin = StringIO(GOOD_ANSWER_BLOCK * len(scenario.stages))
            result = session.run_session(
                scenario,
                stdin=stdin,
                stdout=StringIO(),
                learner="integration-learner",
            )

            transcript = transcripts.validate_transcript(result.transcript_path)
            reviewed = rubric.evaluate(result.transcript_path)

            assert transcript.scenario_id == scenario_id
            assert [stage.kind for stage in transcript.stages][-1] == "closing_feedback"
            assert {stage.kind for stage in transcript.stages[:-1]} == {
                stage.kind for stage in scenario.stages
            }
            assert reviewed.dimensions
            assert all(
                dimension.manual_review or dimension.score is not None
                for dimension in reviewed.dimensions
            )

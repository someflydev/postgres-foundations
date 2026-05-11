from io import StringIO
from unittest.mock import patch

from pgfound.interview import scenario as scenario_loader
from pgfound.interview import session, transcripts


def test_interview_session_writes_well_formed_stubbed_transcript() -> None:
    scenario = scenario_loader.load_scenario("senior-backend-saas-rls")
    stdin = StringIO(
        "I would identify tenant scoped tables because database truth matters.\n"
        "The tradeoff is policy complexity, and what we might consider later is monitoring.\n"
        "/next\n"
        "For RLS I would use constraints, transaction checks, and rollback "
        "planning because leaks matter.\n"
        "This is a tradeoff with debugging overhead and not yet a reason for extra extensions.\n"
        "/next\n"
        "I would reproduce the issue and defend the isolation or lock choice "
        "because correctness matters.\n"
        "/next\n"
        "Partitioning or RLS should wait for workload signals; monitor bloat "
        "and query plans later.\n"
        "The tradeoff is operational burden because migrations become harder.\n"
        "/next\n"
    )
    stdout = StringIO()

    with patch("pgfound.interview.session.exercise_runner.check_answer", return_value=(True, "")):
        result = session.run_session(
            scenario,
            stdin=stdin,
            stdout=stdout,
            learner="test-learner",
        )

    transcript = transcripts.validate_transcript(result.transcript_path)
    output = stdout.getvalue()

    assert transcript.scenario_id == "senior-backend-saas-rls"
    assert len(transcript.stages) == 5
    assert transcript.stages[-1].kind == "closing_feedback"
    assert "What the simulator would send to the LLM" in transcript.raw_text
    assert session.LLM_STUB in transcript.raw_text
    assert "Follow-up questions:" in output
    assert "Overall:" in result.review_summary

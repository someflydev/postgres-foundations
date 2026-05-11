from pgfound.interview import prompts
from pgfound.interview import scenario as scenario_loader


def test_followup_generator_renders_without_error() -> None:
    scenario = scenario_loader.load_scenario("senior-backend-saas-rls")
    stage = scenario.stages[1]

    rendered = prompts.render_follow_ups(
        scenario,
        stage,
        stage_transcript="Learner says RLS is enough because policies protect tenants.",
    )

    assert "Probe" in rendered.text or "1." in rendered.text

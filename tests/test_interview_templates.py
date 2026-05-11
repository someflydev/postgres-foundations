from pgfound.interview import prompts
from pgfound.interview import scenario as scenario_loader
from pgfound.llm import templates


def test_interview_stage_and_persona_templates_render_against_fixture() -> None:
    scenario = scenario_loader.load_scenario("senior-backend-saas-rls")
    base_context = {
        "scenario_id": scenario.id,
        "scenario_title": scenario.title,
        "duration_minutes": scenario.duration_minutes,
        "capability_layers_required": list(scenario.capability_layers_required),
        "rubric_id": scenario.rubric_id,
        "stage_kind": "design_probe",
        "topic": "multi_tenant_rls",
        "exercise_id": "introduction-to-row-level-security-level-c-1",
        "exercise_prompt": "Inspect RLS behavior and defend the verification query.",
        "previous_stages": [],
        "latest_response": "I would start by naming the tenant invariant.",
        "full_transcript": "Learner defended tenant-scoped access.",
    }

    for template_id in (
        "interview/personas/senior-interviewer",
        "interview/personas/mid-interviewer",
        "interview/personas/adversarial-architect",
    ):
        rendered = templates.render_template(template_id, base_context)
        assert "Forbidden Behaviors" in rendered

    for template_id in (
        "interview/stages/warmup",
        "interview/stages/design-probe",
        "interview/stages/debugging-drill-wrap",
        "interview/stages/oral-defense",
        "interview/stages/capstone-defense",
        "interview/stages/closing-feedback",
    ):
        rendered = templates.render_template(template_id, base_context)
        assert rendered.strip()
        assert "=== HIDDEN SIMULATOR NOTES ===" in rendered


def test_interview_scenario_stage_templates_render_through_session_helper() -> None:
    scenario = scenario_loader.load_scenario("senior-backend-saas-rls")

    for stage in scenario.stages:
        rendered = prompts.load_prompt(scenario, stage, previous_stages=[])
        assert rendered.text.strip()


def test_interview_dispatch_templates_are_registered() -> None:
    loaded = {template.id for template in templates.list_templates()}

    assert "interview/personas/senior-interviewer" in loaded
    assert "interview/stages/closing-feedback" in loaded

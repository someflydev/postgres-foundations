import json
from pathlib import Path

from click.testing import CliRunner

from pgfound.cli import main
from pgfound.decision import prompts
from pgfound.llm import templates


def _fixture(name: str) -> dict[str, object]:
    return json.loads(Path(f"tests/fixtures/{name}").read_text(encoding="utf-8"))


def _context_for(template_id: str) -> dict[str, object]:
    evaluator = _fixture("evaluator-context.json")
    critique = _fixture("critique-context.json")
    context: dict[str, object] = {
        **evaluator,
        **critique,
        "catalog_schema": {"type": "object", "required": ["id", "title", "summary"]},
        "existing_entries": [
            {"id": "saas_multi_tenant", "title": "SaaS Multi-tenant", "summary": "Shared tenancy."}
        ],
        "ask": "Add a catalog entry for regulated scheduling operations.",
        "evidence": "Observed in healthcare scheduling products with strict overlap rules.",
        "intake_schema": {"type": "object", "required": ["intake_id", "organization"]},
        "proposed_field": {"name": "latency_slo_ms", "type": "integer"},
        "rationale": "Latency SLOs affect topology and index urgency.",
        "prevalence_evidence": "Common in SaaS and payment processing intakes.",
        "candidate_values": ["100", "250", "500"],
        "rule_schema": {"type": "object", "required": ["id", "target_slug", "verdict"]},
        "real_world_scenario": "A shared-schema SaaS app needs tenant isolation.",
        "recommendation_target": "row_level_security",
        "thin_evidence_notes": "Connection behavior and search needs are under-specified.",
        "audience": "engineering leadership",
        "scenario_brief": "Create a minimal but realistic regression scenario.",
    }
    return context


def test_decision_templates_parse_and_render() -> None:
    loaded = prompts.list_templates()

    assert {template.id for template in loaded} == prompts.DECISION_TEMPLATE_IDS
    for template in loaded:
        rendered = prompts.render_template(template.id, _context_for(template.id))
        assert rendered.strip()


def test_decision_prompt_render_cli_outputs_evaluator_prompt() -> None:
    result = CliRunner().invoke(
        main,
        [
            "decision",
            "prompt",
            "render",
            "layer-2-evaluator/evaluate-intake",
            "--context",
            "tests/fixtures/evaluator-context.json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "saas-multi-tenant-minimal" in result.output
    assert "decision-engine/schemas/report.schema.json" in result.output


def test_decision_prompt_render_cli_outputs_critique_prompt() -> None:
    result = CliRunner().invoke(
        main,
        [
            "decision",
            "prompt",
            "render",
            "layer-4-critique/cross-check-recommendations-against-anti-patterns",
            "--context",
            "tests/fixtures/critique-context.json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Row-level Security" in result.output
    assert "anti-pattern" in result.output.lower()


def test_decision_prompt_list_cli_shows_templates() -> None:
    result = CliRunner().invoke(main, ["decision", "prompt", "list"])

    assert result.exit_code == 0, result.output
    assert "pgfound decision prompts" in result.output


def test_decision_prompt_context_validation_uses_required_inputs() -> None:
    template = prompts.load_template("layer-2-evaluator/evaluate-intake")
    context = templates.merge_context(
        template,
        _context_for(template.id),
        output_format_base=prompts.OUTPUT_FORMAT_BASE,
    )
    templates.validate_inputs(template, context)

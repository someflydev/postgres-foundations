from pgfound.decision import prompts


def test_prompt_output_format_templates_render() -> None:
    output_formats = [
        "shared/output-formats/catalog-entry",
        "shared/output-formats/rule-entry",
        "shared/output-formats/evaluator-output",
        "shared/output-formats/scenario-intake",
        "shared/output-formats/critique-output",
    ]

    for template_id in output_formats:
        rendered = prompts.render_template(template_id, {})
        assert "Required Response Shape" in rendered

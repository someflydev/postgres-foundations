"""Decision-engine prompt-template discovery and rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.llm import templates

OUTPUT_FORMAT_BASE = "decision-engine/prompts/shared/output-formats"

DECISION_TEMPLATE_IDS = {
    "layer-1-schema-catalog/propose-industry-entry",
    "layer-1-schema-catalog/propose-data-shape-entry",
    "layer-1-schema-catalog/propose-workload-pattern-entry",
    "layer-1-schema-catalog/propose-extension-entry",
    "layer-1-schema-catalog/propose-index-pattern-entry",
    "layer-1-schema-catalog/propose-topology-pattern-entry",
    "layer-1-schema-catalog/propose-anti-pattern-entry",
    "layer-1-schema-catalog/refine-intake-schema",
    "layer-1-schema-catalog/propose-rule",
    "layer-2-evaluator/evaluate-intake",
    "layer-2-evaluator/explain-tradeoffs",
    "layer-2-evaluator/generate-followup-questions",
    "layer-2-evaluator/generate-now-later-avoid",
    "layer-3-scenarios/fintech-payments-scenario",
    "layer-3-scenarios/healthcare-ops-scenario",
    "layer-3-scenarios/saas-multi-tenant-scenario",
    "layer-3-scenarios/ecommerce-marketplace-scenario",
    "layer-3-scenarios/logistics-geo-scenario",
    "layer-3-scenarios/observability-iot-scenario",
    "layer-3-scenarios/knowledge-ai-scenario",
    "layer-3-scenarios/modernization-bridge-scenario",
    "layer-4-critique/cross-check-recommendations-against-anti-patterns",
    "layer-4-critique/look-for-overcomplexity",
    "layer-4-critique/test-portability-assumptions",
    "layer-4-critique/generate-benchmark-plan",
    "layer-4-critique/identify-missing-core-features",
    "shared/output-formats/catalog-entry",
    "shared/output-formats/rule-entry",
    "shared/output-formats/evaluator-output",
    "shared/output-formats/scenario-intake",
    "shared/output-formats/critique-output",
    "shared/system-prompt-architect",
}


def load_template(template_id: str) -> templates.PromptTemplate:
    """Load one decision-engine prompt template."""
    return templates.load_template_from_dir(template_id, paths.DECISION_PROMPTS_DIR, "decision")


def list_templates() -> list[templates.PromptTemplate]:
    """Return all decision-engine prompt templates."""
    return templates.list_templates_from_dir(paths.DECISION_PROMPTS_DIR)


def render_template(
    template_id: str,
    context: dict[str, Any],
    *,
    variables: dict[str, Any] | None = None,
) -> str:
    """Render one decision-engine prompt template without calling an LLM."""
    template = load_template(template_id)
    return templates.render_loaded_template(
        template,
        context,
        variables=variables,
        output_format_base=OUTPUT_FORMAT_BASE,
    )


def render_template_to_path(
    template_id: str,
    context: dict[str, Any],
    out_path: Path,
    *,
    variables: dict[str, Any] | None = None,
) -> Path:
    """Render a decision-engine prompt template to a path."""
    rendered = render_template(template_id, context, variables=variables)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return out_path

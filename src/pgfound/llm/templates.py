"""Markdown prompt-template discovery, validation, and rendering."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import StrictUndefined, Template

from pgfound import paths

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)

TRAINING_TEMPLATE_IDS = {
    "capstone-reviewer/extension-posture-review",
    "capstone-reviewer/full-capstone-review",
    "capstone-reviewer/operational-runbook-review",
    "capstone-reviewer/writeup-review",
    "coaching/concept-check",
    "coaching/analogy-generator",
    "coaching/misunderstanding-probe",
    "critique/query-critique",
    "critique/schema-critique",
    "critique/index-critique",
    "critique/concurrency-critique",
    "interview/follow-up-generator",
    "interview/personas/adversarial-architect",
    "interview/personas/mid-interviewer",
    "interview/personas/senior-interviewer",
    "interview/stages/capstone-defense",
    "interview/stages/closing-feedback",
    "interview/stages/debugging-drill-wrap",
    "interview/stages/design-probe",
    "interview/stages/oral-defense",
    "interview/stages/warmup",
    "remediation/remediation-pack-generator",
    "remediation/hint-ladder-generator",
    "remediation/failure-lab-generator",
    "shared/system-prompt-trainer",
}


@dataclass(frozen=True)
class PromptTemplate:
    """Parsed Markdown prompt template."""

    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.metadata["id"])

    @property
    def title(self) -> str:
        return str(self.metadata.get("title", self.id))

    @property
    def inputs(self) -> dict[str, dict[str, Any]]:
        raw = self.metadata.get("inputs", {})
        if not isinstance(raw, dict):
            msg = f"template {self.id} has non-mapping inputs"
            raise ValueError(msg)
        return raw

    @property
    def consumed_by(self) -> tuple[str, ...]:
        raw = self.metadata.get("consumed_by", ())
        return tuple(str(item) for item in raw)


def load_template_from_dir(template_id: str, template_dir: Path, label: str) -> PromptTemplate:
    """Load one template by front-matter id from a prompt-template root."""
    normalized = template_id.removesuffix(".md")
    path = template_dir / f"{normalized}.md"
    if not path.is_file():
        matches = [
            template
            for template in list_templates_from_dir(template_dir)
            if template.id == normalized
        ]
        if not matches:
            msg = f"{label} prompt template not found: {template_id}"
            raise ValueError(msg)
        return matches[0]
    template = parse_template(path)
    if template.id != normalized:
        msg = f"template id {template.id!r} does not match path id {normalized!r}"
        raise ValueError(msg)
    return template


def load_template(template_id: str) -> PromptTemplate:
    """Load one training-side template by front-matter id."""
    return load_template_from_dir(template_id, paths.LLM_PROMPTS_DIR, "LLM")


def list_templates_from_dir(template_dir: Path) -> list[PromptTemplate]:
    """Return all front-matter prompt templates under a template root."""
    templates: list[PromptTemplate] = []
    for path in sorted(template_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not FRONT_MATTER_RE.match(text):
            continue
        template = parse_template(path)
        templates.append(template)
    return templates


def list_templates() -> list[PromptTemplate]:
    """Return all front-matter prompt templates under llm-prompts."""
    return list_templates_from_dir(paths.LLM_PROMPTS_DIR)


def parse_template(path: Path) -> PromptTemplate:
    """Parse YAML front matter and Markdown body from a template path."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        msg = f"template lacks YAML front matter: {path.relative_to(paths.REPO_ROOT)}"
        raise ValueError(msg)
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict) or not metadata.get("id"):
        msg = f"template front matter must include id: {path.relative_to(paths.REPO_ROOT)}"
        raise ValueError(msg)
    return PromptTemplate(path=path, metadata=metadata, body=match.group(2).strip() + "\n")


def render_template(
    template_id: str,
    context: dict[str, Any],
    *,
    variables: dict[str, Any] | None = None,
) -> str:
    """Validate and render one template with Jinja2."""
    template = load_template(template_id)
    merged = merge_context(template, context, variables=variables)
    validate_inputs(template, merged)
    return Template(template.body, undefined=StrictUndefined).render(**merged)


def render_loaded_template(
    template: PromptTemplate,
    context: dict[str, Any],
    *,
    variables: dict[str, Any] | None = None,
    output_format_base: str = "llm-prompts/shared/output-formats",
) -> str:
    """Validate and render an already loaded template."""
    merged = merge_context(
        template,
        context,
        variables=variables,
        output_format_base=output_format_base,
    )
    validate_inputs(template, merged)
    return Template(template.body, undefined=StrictUndefined).render(**merged)


def render_template_to_path(
    template_id: str,
    context: dict[str, Any],
    out_path: Path,
    *,
    variables: dict[str, Any] | None = None,
) -> Path:
    """Render a template and write it to a path."""
    rendered = render_template(template_id, context, variables=variables)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def merge_context(
    template: PromptTemplate,
    context: dict[str, Any],
    *,
    variables: dict[str, Any] | None = None,
    output_format_base: str = "llm-prompts/shared/output-formats",
) -> dict[str, Any]:
    """Merge template variables, context JSON, and CLI overrides."""
    merged: dict[str, Any] = {}
    template_variables = template.metadata.get("variables", {})
    if isinstance(template_variables, dict):
        merged.update(template_variables)
    merged.update(context)
    if variables:
        merged.update(variables)
    output_format = template.metadata.get("outputs", {}).get("format")
    if output_format:
        merged.setdefault("output_format_ref", f"{output_format_base}/{output_format}.md")
    return merged


def validate_inputs(template: PromptTemplate, context: dict[str, Any]) -> None:
    """Validate required inputs declared in template front matter."""
    missing = []
    wrong_kind = []
    for name, schema in template.inputs.items():
        required = bool(schema.get("required", False))
        if required and name not in context:
            missing.append(name)
            continue
        if name not in context:
            continue
        expected_kind = schema.get("kind")
        if expected_kind == "list" and not isinstance(context[name], list | tuple):
            wrong_kind.append(f"{name} must be a list")
        if expected_kind == "mapping" and not isinstance(context[name], dict):
            wrong_kind.append(f"{name} must be an object")
    if missing or wrong_kind:
        detail = "; ".join([f"missing: {', '.join(missing)}", *wrong_kind]).strip("; ")
        msg = f"invalid context for {template.id}: {detail}"
        raise ValueError(msg)


def load_context(path: Path) -> dict[str, Any]:
    """Load a JSON context object."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        msg = "context JSON must be an object"
        raise ValueError(msg)
    return payload


def parse_var_overrides(items: tuple[str, ...]) -> dict[str, Any]:
    """Parse repeated key=value CLI overrides."""
    parsed: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            msg = f"--var must be key=value, got {item!r}"
            raise ValueError(msg)
        key, value = item.split("=", 1)
        try:
            parsed[key] = json.loads(value)
        except json.JSONDecodeError:
            parsed[key] = value
    return parsed

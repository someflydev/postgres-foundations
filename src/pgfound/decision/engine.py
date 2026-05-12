"""Decision engine stub implementation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from pgfound import paths

Report = dict[str, Any]

ENGINE_VERSION = "0.1.0-prompt39"
SCHEMA_URI_BASE = "https://postgres-foundations/schema/"


class DecisionValidationError(ValueError):
    """Raised when a decision-engine document fails schema validation."""


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in {path}: {exc}"
        raise DecisionValidationError(msg) from exc


def _schema_registry() -> Registry:
    resources: list[tuple[str, Resource]] = []
    for schema_path in (paths.DECISION_ENGINE_DIR / "schemas").glob("*.schema.json"):
        schema = _load_json(schema_path)
        resource = Resource.from_contents(schema)
        resources.append((schema_path.name, resource))
        resources.append((f"{SCHEMA_URI_BASE}{schema_path.name}", resource))
    return Registry().with_resources(resources)


def _validate(instance: Any, schema_name: str) -> None:
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / schema_name
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema, registry=_schema_registry())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        raise DecisionValidationError(_format_validation_errors(schema_name, errors))


def _format_validation_errors(schema_name: str, errors: list[ValidationError]) -> str:
    lines = [f"{schema_name} validation failed:"]
    for error in errors:
        location = ".".join(str(part) for part in error.path) or "$"
        lines.append(f"- {location}: {error.message}")
    return "\n".join(lines)


def _catalog_and_rule_warnings() -> list[str]:
    warnings: list[str] = []
    for label, directory in (
        ("catalogs", paths.DECISION_ENGINE_DIR / "catalogs"),
        ("rules", paths.DECISION_ENGINE_DIR / "rules"),
    ):
        authored_files = [
            path
            for path in directory.glob("*.json")
            if path.is_file() and not path.name.startswith(".")
        ]
        if not authored_files:
            warnings.append(f"{label} not yet authored; decision output is intentionally empty")
    return warnings


def validate_report(report: Report) -> None:
    """Validate a generated report against the report schema."""
    _validate(report, "report.schema.json")


def run_decision(intake_path: str | Path) -> Report:
    """Validate an intake and return an empty-but-valid decision report."""
    intake_file = Path(intake_path)
    intake = _load_json(intake_file)
    _validate(intake, "intake.schema.json")

    report: Report = {
        "intake_id": intake["intake_id"],
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "engine_version": ENGINE_VERSION,
        "recommendations": [],
        "score_breakdown": {
            "domain_fit": 0.0,
            "data_shape_fit": 0.0,
            "workload_fit": 0.0,
            "operational_feasibility": 0.0,
            "growth_urgency": 0.0,
            "portability_penalty": 0.0,
            "complexity_penalty": 0.0,
        },
        "warnings": [
            {"anti_pattern_slug": "catalogs_not_yet_authored", "message": warning}
            for warning in _catalog_and_rule_warnings()
        ],
        "followup_questions": [],
    }
    validate_report(report)
    return report

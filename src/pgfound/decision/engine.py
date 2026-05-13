"""Decision engine implementation and catalog validation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from pgfound import paths

Report = dict[str, Any]

ENGINE_VERSION = "0.2.0-prompt42"
SCHEMA_URI_BASE = "https://postgres-foundations/schema/"
CATALOG_KINDS = {
    "industry": ("industries.json", "industry.schema.json"),
    "data_shape": ("data_shapes.json", "data-shape.schema.json"),
    "workload_pattern": ("workload_patterns.json", "workload-pattern.schema.json"),
    "core_feature": ("postgres_core_features.json", "core-feature.schema.json"),
    "extension": ("extensions.json", "extension.schema.json"),
    "index_pattern": ("index_patterns.json", "index-pattern.schema.json"),
    "topology_pattern": ("topology_patterns.json", "topology-pattern.schema.json"),
    "anti_pattern": ("anti_patterns.json", "anti-pattern.schema.json"),
}
CATALOG_DIR = paths.DECISION_ENGINE_DIR / "catalogs"


class DecisionValidationError(ValueError):
    """Raised when a decision-engine document fails schema validation."""


class CatalogCheckResult(dict[str, list[str]]):
    """Container for catalog check errors and warnings."""


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


def _catalog_path(kind: str) -> Path:
    try:
        filename, _ = CATALOG_KINDS[kind]
    except KeyError as exc:
        expected = ", ".join(sorted(CATALOG_KINDS))
        msg = f"unknown catalog kind {kind!r}; expected one of: {expected}"
        raise DecisionValidationError(msg) from exc
    return CATALOG_DIR / filename


def _catalog_present(kind: str) -> bool:
    return _catalog_path(kind).is_file()


def load_catalog(kind: str) -> list[dict[str, Any]]:
    """Load and schema-validate one authored catalog."""
    path = _catalog_path(kind)
    if not path.is_file():
        return []
    catalog = _load_json(path)
    if not isinstance(catalog, list):
        raise DecisionValidationError(f"{path} must be a JSON array")

    _, schema_name = CATALOG_KINDS[kind]
    for entry in catalog:
        _validate(entry, schema_name)
    return catalog


def load_catalog_index(kind: str) -> dict[str, dict[str, Any]]:
    """Return a catalog keyed by slug, rejecting duplicate ids."""
    entries = load_catalog(kind)
    index: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for entry in entries:
        slug = str(entry["id"])
        if slug in index:
            duplicates.append(slug)
        index[slug] = entry
    if duplicates:
        raise DecisionValidationError(
            f"{kind} catalog has duplicate ids: {', '.join(sorted(set(duplicates)))}"
        )
    return index


def _sentence_count(text: str) -> int:
    return sum(1 for chunk in text.replace("?", ".").replace("!", ".").split(".") if chunk.strip())


def check_catalogs() -> CatalogCheckResult:
    """Run cross-catalog and authoring sanity checks."""
    errors: list[str] = []
    warnings: list[str] = []

    catalogs: dict[str, dict[str, dict[str, Any]]] = {}
    for kind in CATALOG_KINDS:
        try:
            catalogs[kind] = load_catalog_index(kind)
        except DecisionValidationError as exc:
            errors.append(str(exc))
            catalogs[kind] = {}

    data_shape_ids = set(catalogs["data_shape"])
    workload_ids = set(catalogs["workload_pattern"])
    core_feature_ids = set(catalogs["core_feature"])
    extension_ids = set(catalogs["extension"])
    index_pattern_ids = set(catalogs["index_pattern"])
    topology_pattern_ids = set(catalogs["topology_pattern"])
    anti_pattern_ids = set(catalogs["anti_pattern"])
    referenced_data_shapes: set[str] = set()
    referenced_workloads: set[str] = set()

    for kind, entries in catalogs.items():
        for entry in entries.values():
            title = str(entry.get("title", "")).strip()
            summary = str(entry.get("summary", "")).strip()
            if not title:
                errors.append(f"{kind}:{entry.get('id', '<missing>')} has an empty title")
            if _sentence_count(summary) < 2:
                entry_id = entry.get("id", "<missing>")
                errors.append(f"{kind}:{entry_id} summary must have >= 2 sentences")

    for industry in catalogs["industry"].values():
        industry_id = industry["id"]
        for slug in industry["typical_data_shapes"]:
            referenced_data_shapes.add(slug)
            if slug not in data_shape_ids:
                errors.append(f"industry:{industry_id} references missing data_shape:{slug}")
        for slug in industry["typical_workload_patterns"]:
            referenced_workloads.add(slug)
            if slug not in workload_ids:
                errors.append(f"industry:{industry_id} references missing workload_pattern:{slug}")

    for slug in sorted(data_shape_ids - referenced_data_shapes):
        warnings.append(f"data_shape:{slug} is not referenced by any industry")
    for slug in sorted(workload_ids - referenced_workloads):
        warnings.append(f"workload_pattern:{slug} is not referenced by any industry")

    for kind in ("data_shape", "workload_pattern"):
        for entry in catalogs[kind].values():
            for slug in entry.get("core_features_that_apply", []):
                if slug not in core_feature_ids:
                    errors.append(f"{kind}:{entry['id']} references missing core_feature:{slug}")
            for slug in entry.get("extensions_that_apply", []):
                if slug not in extension_ids:
                    errors.append(f"{kind}:{entry['id']} references missing extension:{slug}")
            for slug in entry.get("index_patterns_that_apply", []):
                if slug not in index_pattern_ids:
                    errors.append(f"{kind}:{entry['id']} references missing index_pattern:{slug}")
            for slug in entry.get("topology_patterns_that_apply", []):
                if slug not in topology_pattern_ids:
                    errors.append(
                        f"{kind}:{entry['id']} references missing topology_pattern:{slug}"
                    )
            for slug in entry.get("anti_patterns_to_watch", []):
                if slug not in anti_pattern_ids:
                    errors.append(f"{kind}:{entry['id']} references missing anti_pattern:{slug}")

    for core_feature in catalogs["core_feature"].values():
        for slug in core_feature["applies_to_data_shapes"]:
            if slug not in data_shape_ids:
                errors.append(
                    f"core_feature:{core_feature['id']} references missing data_shape:{slug}"
                )
        for slug in core_feature["applies_to_workload_patterns"]:
            if slug not in workload_ids:
                errors.append(
                    f"core_feature:{core_feature['id']} references missing workload_pattern:{slug}"
                )

    for extension in catalogs["extension"].values():
        for slug in extension["adoption_triggers"]:
            if slug not in workload_ids:
                errors.append(
                    f"extension:{extension['id']} references missing adoption trigger:{slug}"
                )
        for slug in extension["avoidance_triggers"]:
            if slug not in workload_ids and slug not in anti_pattern_ids:
                errors.append(
                    f"extension:{extension['id']} references missing avoidance trigger:{slug}"
                )
        for slug in extension["prereq_extensions"]:
            if slug not in extension_ids:
                errors.append(f"extension:{extension['id']} references missing prereq:{slug}")
        for slug in extension["anti_patterns"]:
            if slug not in anti_pattern_ids:
                errors.append(f"extension:{extension['id']} references missing anti_pattern:{slug}")

    module_ids: set[str] = set()
    extension_map_path = paths.CURRICULUM_DIR / "extensions" / "map.json"
    if extension_map_path.is_file():
        extension_map = _load_json(extension_map_path)
        module_ids.update(str(module["id"]) for module in extension_map.get("modules", []))
    module_ids.update(
        path.parent.name for path in (paths.LESSONS_DIR).glob("phase-*/*/*/lesson.json")
    )
    for extension in catalogs["extension"].values():
        module_slug = extension["module_slug"]
        if module_slug not in module_ids:
            errors.append(
                f"extension:{extension['id']} references missing module_slug:{module_slug}"
            )

    for index_pattern in catalogs["index_pattern"].values():
        for slug in index_pattern["applies_to_data_shapes"]:
            if slug not in data_shape_ids:
                errors.append(
                    f"index_pattern:{index_pattern['id']} references missing data_shape:{slug}"
                )
        for slug in index_pattern["applies_to_workload_patterns"]:
            if slug not in workload_ids:
                errors.append(
                    f"index_pattern:{index_pattern['id']} "
                    f"references missing workload_pattern:{slug}"
                )

    for topology_pattern in catalogs["topology_pattern"].values():
        for slug in topology_pattern["applies_to_workload_patterns"]:
            if slug not in workload_ids:
                errors.append(
                    f"topology_pattern:{topology_pattern['id']} "
                    f"references missing workload_pattern:{slug}"
                )

    for anti_pattern in catalogs["anti_pattern"].values():
        for reference in anti_pattern["references"]:
            if not (paths.REPO_ROOT / reference).is_file():
                errors.append(
                    f"anti_pattern:{anti_pattern['id']} references missing doc:{reference}"
                )

    return CatalogCheckResult(errors=errors, warnings=warnings)


def validate_intake_references(intake: dict[str, Any]) -> None:
    """Enforce intake slugs against authored catalogs."""
    errors: list[str] = []
    if _catalog_present("industry"):
        industries = load_catalog_index("industry")
        industry = intake["organization"]["industry"]
        if industry not in industries:
            errors.append(f"intake references missing industry:{industry}")
    if _catalog_present("data_shape"):
        data_shapes = load_catalog_index("data_shape")
        for slug in intake["data_shapes"]:
            if slug not in data_shapes:
                errors.append(f"intake references missing data_shape:{slug}")
    if _catalog_present("workload_pattern"):
        workloads = load_catalog_index("workload_pattern")
        for slug in intake["workload_patterns"]:
            if slug not in workloads:
                errors.append(f"intake references missing workload_pattern:{slug}")
    if errors:
        raise DecisionValidationError("\n".join(errors))


def validate_report(report: Report) -> None:
    """Validate a generated report against the report schema."""
    _validate(report, "report.schema.json")


def run_decision(intake_path: str | Path, rule_pattern: str | None = None) -> Report:
    """Validate an intake and return a populated decision report."""
    from pgfound.decision import evaluator

    intake_file = Path(intake_path)
    intake = _load_json(intake_file)
    _validate(intake, "intake.schema.json")
    validate_intake_references(intake)
    evaluated = evaluator.evaluate(intake, rule_pattern=rule_pattern)

    report: Report = {
        "intake_id": intake["intake_id"],
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "engine_version": ENGINE_VERSION,
        "recommendations": evaluated["recommendations"],
        "score_breakdown": evaluated["score_breakdown"],
        "warnings": [
            {
                "anti_pattern_slug": recommendation["target_slug"],
                "message": "; ".join(recommendation["why_now"])
                or f"{recommendation['target_slug']} warning triggered",
            }
            for recommendation in evaluated["recommendations"]
            if recommendation["kind"] == "anti_pattern_warning"
        ],
        "followup_questions": evaluated["followup_questions"],
    }
    validate_report(report)
    return report


def explain_decision(
    intake_path: str | Path,
    target_slug: str,
    rule_pattern: str | None = None,
) -> list[dict[str, str]]:
    """Return rule explanations for one target slug."""
    from pgfound.decision import evaluator

    intake_file = Path(intake_path)
    intake = _load_json(intake_file)
    _validate(intake, "intake.schema.json")
    validate_intake_references(intake)
    evaluated = evaluator.evaluate(intake, rule_pattern=rule_pattern)
    return evaluated["explain"].get(target_slug, [])

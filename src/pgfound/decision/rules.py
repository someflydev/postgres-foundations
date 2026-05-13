"""Decision rule loading, matching, and linting."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.decision import engine

RULE_DIR = paths.DECISION_ENGINE_DIR / "rules"
PREDICATE_KEYS = {
    "industry_is",
    "industry_in",
    "data_shape_present",
    "data_shape_any_of",
    "data_shape_all_of",
    "workload_pattern_present",
    "workload_pattern_any_of",
    "scale_signal_gte",
    "scale_signal_lt",
    "tenancy_model_is",
    "tenancy_model_in",
    "security_constraint_present",
    "portability_constraint_present",
    "operational_tolerance_is",
    "existing_topology_is",
    "migration_need",
    "free_form_notes_contains",
    "explicit_bias_for_contains",
    "explicit_bias_against_contains",
}
TARGET_KIND_TO_CATALOG = {
    "core_feature": "core_feature",
    "extension": "extension",
    "index_pattern": "index_pattern",
    "topology_pattern": "topology_pattern",
    "anti_pattern_warning": "anti_pattern",
}


@dataclass(frozen=True)
class RuleMatch:
    rule: dict[str, Any]
    actions: list[dict[str, Any]]


class RuleLintResult(dict[str, list[str]]):
    """Container for decision-rule lint errors and warnings."""


def _rule_files(pattern: str | None = None) -> list[Path]:
    files = sorted(path for path in RULE_DIR.rglob("*.json") if path.is_file())
    if not pattern:
        return files
    return [
        path
        for path in files
        if fnmatch.fnmatch(str(path), pattern)
        or fnmatch.fnmatch(str(path.relative_to(paths.REPO_ROOT)), pattern)
        or fnmatch.fnmatch(path.name, pattern)
    ]


def load_rules(pattern: str | None = None) -> list[dict[str, Any]]:
    """Load and schema-validate rule files."""
    rules: list[dict[str, Any]] = []
    for path in _rule_files(pattern):
        rule = engine._load_json(path)  # noqa: SLF001 - shared local validator helper.
        engine._validate(rule, "rule.schema.json")  # noqa: SLF001
        rules.append(rule)
    return rules


def _largest_table_rows(intake: dict[str, Any]) -> float:
    row_counts = intake.get("scale_signals", {}).get("row_counts_largest_tables", {})
    return float(max(row_counts.values(), default=0))


def _scale_value(intake: dict[str, Any], key: str) -> float:
    if key == "largest_table_rows":
        return _largest_table_rows(intake)
    value = intake.get("scale_signals", {}).get(key, 0)
    return float(value or 0)


def predicate_matches(predicate: dict[str, Any], intake: dict[str, Any]) -> bool:
    """Evaluate one predicate against one intake."""
    key, expected = next(iter(predicate.items()))
    if key == "industry_is":
        return intake["organization"]["industry"] == expected
    if key == "industry_in":
        return intake["organization"]["industry"] in expected
    if key == "data_shape_present":
        return expected in intake["data_shapes"]
    if key == "data_shape_any_of":
        return any(slug in intake["data_shapes"] for slug in expected)
    if key == "data_shape_all_of":
        return all(slug in intake["data_shapes"] for slug in expected)
    if key == "workload_pattern_present":
        return expected in intake["workload_patterns"]
    if key == "workload_pattern_any_of":
        return any(slug in intake["workload_patterns"] for slug in expected)
    if key == "scale_signal_gte":
        return _scale_value(intake, expected["key"]) >= float(expected["value"])
    if key == "scale_signal_lt":
        return _scale_value(intake, expected["key"]) < float(expected["value"])
    if key == "tenancy_model_is":
        return intake["tenancy_model"] == expected
    if key == "tenancy_model_in":
        return intake["tenancy_model"] in expected
    if key == "security_constraint_present":
        return expected in intake["security_constraints"]
    if key == "portability_constraint_present":
        return expected in intake["organization"]["portability_constraints"]
    if key == "operational_tolerance_is":
        return intake["organization"]["operational_tolerance"] == expected
    if key == "existing_topology_is":
        return intake["existing_postgres_topology"] == expected
    if key == "migration_need":
        return bool(intake["migration_or_federation_needs"].get(expected))
    if key == "free_form_notes_contains":
        return str(expected).lower() in intake["free_form_notes"].lower()
    if key == "explicit_bias_for_contains":
        return any(item["extension_slug"] == expected for item in intake["explicit_bias_for"])
    if key == "explicit_bias_against_contains":
        return any(item["extension_slug"] == expected for item in intake["explicit_bias_against"])
    return False


def rule_matches(rule: dict[str, Any], intake: dict[str, Any]) -> bool:
    """Return whether an active rule triggers for an intake."""
    if rule["status"] != "active":
        return False
    when = rule.get("when", {})
    if_all = when.get("if_all", [])
    if_any = when.get("if_any", [])
    if_not = when.get("if_not", [])
    return (
        all(predicate_matches(predicate, intake) for predicate in if_all)
        and (not if_any or any(predicate_matches(predicate, intake) for predicate in if_any))
        and not any(predicate_matches(predicate, intake) for predicate in if_not)
    )


def matching_rules(rules: list[dict[str, Any]], intake: dict[str, Any]) -> list[RuleMatch]:
    """Return active rule matches and their actions."""
    return [
        RuleMatch(rule=rule, actions=rule["then"])
        for rule in rules
        if rule_matches(rule, intake)
    ]


def _predicate_key(predicate: dict[str, Any]) -> str:
    return next(iter(predicate))


def _has_contradictory_if_all(rule: dict[str, Any]) -> bool:
    equalities: dict[str, set[str]] = {}
    for predicate in rule.get("when", {}).get("if_all", []):
        key, value = next(iter(predicate.items()))
        equality_keys = {
            "industry_is",
            "tenancy_model_is",
            "operational_tolerance_is",
            "existing_topology_is",
        }
        if key in equality_keys:
            equalities.setdefault(key, set()).add(str(value))
    return any(len(values) > 1 for values in equalities.values())


def lint_rules(pattern: str | None = None) -> RuleLintResult:
    """Lint rule files against schemas, catalogs, and simple reachability checks."""
    errors: list[str] = []
    warnings: list[str] = []
    rules: list[dict[str, Any]] = []
    for path in _rule_files(pattern):
        try:
            rule = engine._load_json(path)  # noqa: SLF001
            engine._validate(rule, "rule.schema.json")  # noqa: SLF001
        except engine.DecisionValidationError as exc:
            errors.append(f"{path.relative_to(paths.REPO_ROOT)}: {exc}")
            continue
        rules.append(rule)

    catalog_indexes: dict[str, dict[str, dict[str, Any]]] = {}
    for kind in TARGET_KIND_TO_CATALOG.values():
        try:
            catalog_indexes[kind] = engine.load_catalog_index(kind)
        except engine.DecisionValidationError as exc:
            errors.append(str(exc))
            catalog_indexes[kind] = {}

    seen_ids: set[str] = set()
    for rule in rules:
        rule_id = rule["id"]
        if rule_id in seen_ids:
            errors.append(f"duplicate rule id:{rule_id}")
        seen_ids.add(rule_id)

        if _has_contradictory_if_all(rule):
            errors.append(f"rule:{rule_id} has contradictory if_all equality predicates")

        for group_name in ("if_all", "if_any", "if_not"):
            for predicate in rule.get("when", {}).get(group_name, []):
                key = _predicate_key(predicate)
                if key not in PREDICATE_KEYS:
                    errors.append(f"rule:{rule_id} uses unknown predicate:{key}")

        for action in rule["then"]:
            catalog_kind = TARGET_KIND_TO_CATALOG[action["kind"]]
            target_slug = action["target_slug"]
            if target_slug not in catalog_indexes[catalog_kind]:
                errors.append(f"rule:{rule_id} references missing {catalog_kind}:{target_slug}")
            if action["kind"] == "anti_pattern_warning" and action["verdict"] != "avoid_for_now":
                errors.append(f"rule:{rule_id} anti-pattern action must use avoid_for_now")
            if action["verdict"] == "recommend_now" and action["confidence"] < 0.4:
                errors.append(f"rule:{rule_id} recommend_now confidence must be >= 0.4")

    extension_rules = {
        action["target_slug"]
        for rule in rules
        if rule["status"] == "active"
        for action in rule["then"]
        if action["kind"] == "extension"
    }
    for extension_slug in sorted(catalog_indexes.get("extension", {})):
        if extension_slug not in extension_rules:
            warnings.append(f"extension:{extension_slug} has no active rule")

    return RuleLintResult(errors=errors, warnings=warnings)

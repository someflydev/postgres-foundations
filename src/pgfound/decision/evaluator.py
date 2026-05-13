"""Decision rule evaluator."""

from __future__ import annotations

from typing import Any

from pgfound.decision import engine, rules, scoring


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _merge_verdict(
    existing: str,
    incoming: str,
    incoming_confidence: float,
    confidence: float,
) -> str:
    if incoming_confidence > confidence:
        return incoming
    if incoming_confidence == confidence:
        priority = {
            "avoid_for_now": 4,
            "recommend_now": 3,
            "candidate_later": 2,
            "not_enough_evidence": 1,
        }
        return incoming if priority.get(incoming, 0) > priority.get(existing, 0) else existing
    return existing


def _catalog_indexes() -> dict[str, dict[str, dict[str, Any]]]:
    indexes: dict[str, dict[str, dict[str, Any]]] = {}
    for kind in rules.TARGET_KIND_TO_CATALOG.values():
        indexes[kind] = engine.load_catalog_index(kind)
    return indexes


def _followup_cluster(question: str) -> str:
    lowered = question.lower()
    clusters = {
        "geospatial": ("geo", "spatial", "coordinate", "distance", "route"),
        "search": ("search", "lexical", "semantic", "embedding", "vector"),
        "operations": ("restore", "backup", "runbook", "owner", "operate", "pool"),
        "migration": ("migration", "federation", "fdw", "cutover", "legacy"),
        "scale": ("scale", "throughput", "growth", "latency", "rows"),
        "security": ("tenant", "rls", "security", "permission", "pii"),
    }
    for name, tokens in clusters.items():
        if any(token in lowered for token in tokens):
            return name
    return "general"


def _cluster_followups(questions: list[str]) -> dict[str, list[str]]:
    clustered: dict[str, list[str]] = {}
    for question in _dedupe(questions):
        clustered.setdefault(_followup_cluster(question), []).append(question)
    return clustered


def _downgrade_recommendation(recommendation: dict[str, Any]) -> None:
    score = recommendation["recommendation_score"]
    original = recommendation["original_verdict"]
    if original != "recommend_now" or recommendation["kind"] == "anti_pattern_warning":
        recommendation["recommendation_class"] = recommendation["verdict"]
        return
    if score >= 0.65:
        recommendation["recommendation_class"] = "recommend_now"
        recommendation["verdict"] = "recommend_now"
        return
    if score >= 0.4:
        recommendation["verdict"] = "candidate_later"
        recommendation["recommendation_class"] = "candidate_later"
        item = (
            "The rule matched, but weighted score is below the recommend-now threshold; "
            "confirm operational ownership, portability posture, and workload evidence first."
        )
        recommendation["why_not_yet"] = _dedupe(recommendation["why_not_yet"] + [item])
        return
    recommendation["verdict"] = "not_enough_evidence"
    recommendation["recommendation_class"] = "not_enough_evidence"
    recommendation["followup_questions"] = _dedupe(
        recommendation.get("followup_questions", [])
        + [
            f"What evidence would prove {recommendation['target_slug']} is needed now?",
            "Who will own the operational runbook and rollback criteria?",
        ]
    )


def evaluate(intake: dict[str, Any], rule_pattern: str | None = None) -> dict[str, Any]:
    """Run matching rules and return recommendations plus explanation metadata."""
    loaded_rules = rules.load_rules(rule_pattern)
    matches = rules.matching_rules(loaded_rules, intake)
    catalogs = _catalog_indexes()
    by_target: dict[tuple[str, str], dict[str, Any]] = {}
    followup_questions: list[str] = []
    explain: dict[str, list[dict[str, str]]] = {}

    for match in matches:
        rule = match.rule
        for action in match.actions:
            if action["verdict"] == "request_more_information":
                followup_questions.extend(action.get("followup_questions", []))
                continue

            target_key = (action["kind"], action["target_slug"])
            existing = by_target.get(target_key)
            source = {"rule_id": rule["id"], "contribution": action["confidence"]}
            catalog_kind = rules.TARGET_KIND_TO_CATALOG[action["kind"]]
            catalog_entry = catalogs[catalog_kind].get(action["target_slug"], {})
            scored = (
                scoring.score_action(action, intake, catalog_entry)
                if action["kind"] != "anti_pattern_warning"
                else {
                    "score_breakdown": scoring.empty_score_breakdown(),
                    "recommendation_score": float(action["confidence"]),
                }
            )
            explanation = {
                "rule_id": rule["id"],
                "title": rule["title"],
                "verdict": action["verdict"],
                "why": " ".join(action["why_now"] or action["why_not_yet"]),
            }
            explain.setdefault(action["target_slug"], []).append(explanation)
            if existing is None:
                by_target[target_key] = {
                    "kind": action["kind"],
                    "target_slug": action["target_slug"],
                    "verdict": action["verdict"],
                    "original_verdict": action["verdict"],
                    "recommendation_class": action["verdict"],
                    "confidence": action["confidence"],
                    "recommendation_score": scored["recommendation_score"],
                    "score_breakdown": scored["score_breakdown"],
                    "why_now": list(action["why_now"]),
                    "why_not_yet": list(action["why_not_yet"]),
                    "triggers_for_next_stage": list(action["triggers_for_next_stage"]),
                    "followup_questions": list(action.get("followup_questions", [])),
                    "sources": [source],
                    "title": catalog_entry.get("title", action["target_slug"]),
                    "module_slug": catalog_entry.get("module_slug"),
                }
                continue

            existing["verdict"] = _merge_verdict(
                existing["verdict"],
                action["verdict"],
                action["confidence"],
                existing["confidence"],
            )
            previous_confidence = existing["confidence"]
            existing["confidence"] = max(existing["confidence"], action["confidence"])
            if scored["recommendation_score"] > existing["recommendation_score"]:
                existing["recommendation_score"] = scored["recommendation_score"]
                existing["score_breakdown"] = scored["score_breakdown"]
            if action["confidence"] > previous_confidence:
                existing["original_verdict"] = action["verdict"]
            existing["why_now"] = _dedupe(existing["why_now"] + action["why_now"])
            existing["why_not_yet"] = _dedupe(existing["why_not_yet"] + action["why_not_yet"])
            existing["triggers_for_next_stage"] = _dedupe(
                existing["triggers_for_next_stage"] + action["triggers_for_next_stage"]
            )
            existing["followup_questions"] = _dedupe(
                existing["followup_questions"] + action.get("followup_questions", [])
            )
            existing["sources"].append(source)

    for recommendation in by_target.values():
        _downgrade_recommendation(recommendation)
        followup_questions.extend(recommendation.get("followup_questions", []))

    recommendations = sorted(
        by_target.values(),
        key=lambda item: (
            {
                "recommend_now": 0,
                "candidate_later": 1,
                "not_enough_evidence": 2,
                "avoid_for_now": 3,
            }.get(item["recommendation_class"], 4),
            -item["recommendation_score"],
            item["kind"],
            item["target_slug"],
        ),
    )
    scored_recommendations = [
        item for item in recommendations if item["kind"] != "anti_pattern_warning"
    ]
    overall: dict[str, dict[str, float]] = {}
    for recommendation_class in (
        "recommend_now",
        "candidate_later",
        "not_enough_evidence",
        "avoid_for_now",
    ):
        group = [
            item
            for item in scored_recommendations
            if item["recommendation_class"] == recommendation_class
        ]
        if group:
            overall[recommendation_class] = {
                "score": round(sum(item["recommendation_score"] for item in group) / len(group), 3),
                "count": len(group),
            }
    return {
        "recommendations": recommendations,
        "score_breakdown": scoring.average_breakdowns(scored_recommendations),
        "overall": overall,
        "followup_questions": _dedupe(followup_questions),
        "followup_question_groups": _cluster_followups(followup_questions),
        "explain": explain,
    }

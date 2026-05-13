"""Decision rule evaluator."""

from __future__ import annotations

from typing import Any

from pgfound.decision import rules, scoring


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


def evaluate(intake: dict[str, Any], rule_pattern: str | None = None) -> dict[str, Any]:
    """Run matching rules and return recommendations plus explanation metadata."""
    loaded_rules = rules.load_rules(rule_pattern)
    matches = rules.matching_rules(loaded_rules, intake)
    by_target: dict[tuple[str, str], dict[str, Any]] = {}
    followup_questions: list[str] = []
    scoring_actions: list[dict[str, Any]] = []
    explain: dict[str, list[dict[str, str]]] = {}

    for match in matches:
        rule = match.rule
        for action in match.actions:
            if action["verdict"] == "request_more_information":
                followup_questions.extend(action.get("followup_questions", []))
                continue

            scoring_actions.append(action)
            target_key = (action["kind"], action["target_slug"])
            existing = by_target.get(target_key)
            source = {"rule_id": rule["id"], "contribution": action["confidence"]}
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
                    "confidence": action["confidence"],
                    "why_now": list(action["why_now"]),
                    "why_not_yet": list(action["why_not_yet"]),
                    "triggers_for_next_stage": list(action["triggers_for_next_stage"]),
                    "sources": [source],
                }
                continue

            existing["verdict"] = _merge_verdict(
                existing["verdict"],
                action["verdict"],
                action["confidence"],
                existing["confidence"],
            )
            existing["confidence"] = max(existing["confidence"], action["confidence"])
            existing["why_now"] = _dedupe(existing["why_now"] + action["why_now"])
            existing["why_not_yet"] = _dedupe(existing["why_not_yet"] + action["why_not_yet"])
            existing["triggers_for_next_stage"] = _dedupe(
                existing["triggers_for_next_stage"] + action["triggers_for_next_stage"]
            )
            existing["sources"].append(source)

    recommendations = sorted(
        by_target.values(),
        key=lambda item: (
            0 if item["verdict"] == "recommend_now" else 1,
            -item["confidence"],
            item["kind"],
            item["target_slug"],
        ),
    )
    return {
        "recommendations": recommendations,
        "score_breakdown": scoring.average_scoring(scoring_actions),
        "followup_questions": _dedupe(followup_questions),
        "explain": explain,
    }

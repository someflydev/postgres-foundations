"""Comparison normalization helpers for exercise review."""

from __future__ import annotations

import json
import re
from decimal import Decimal
from typing import Any

ARRAY_TEXT_RE = re.compile(r"^\{(?P<body>.*)\}$")
RANGE_TEXT_RE = re.compile(
    r"^\s*(?P<lower_bound>[\[(])\s*(?P<lower>[^,]*)\s*,\s*"
    r"(?P<upper>[^\]\)]*)\s*(?P<upper_bound>[\])])\s*$"
)


def normalize_for_comparison(value: object) -> object:
    """Return a stable representation for row-set answer comparison."""
    if value is None:
        return None
    if isinstance(value, dict):
        return {
            str(key): normalize_for_comparison(value[key])
            for key in sorted(value, key=lambda item: str(item))
        }
    if _looks_like_range_object(value):
        return _normalize_range_object(value)
    if isinstance(value, list | tuple | set):
        return normalize_array(value)
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, str):
        return _normalize_string(value)
    return str(value)


def normalize_array(values: list[Any] | tuple[Any, ...] | set[Any]) -> list[object]:
    """Normalize array-like values with deterministic element ordering."""
    normalized = [normalize_for_comparison(item) for item in values]
    return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True))


def normalize_range_text(value: str) -> str:
    """Normalize textual range bounds without changing inclusivity semantics."""
    stripped = value.strip()
    if stripped.lower() == "empty":
        return "empty"
    match = RANGE_TEXT_RE.match(stripped)
    if match is None:
        return stripped
    return (
        f"{match.group('lower_bound')}"
        f"{match.group('lower').strip()},"
        f"{match.group('upper').strip()}"
        f"{match.group('upper_bound')}"
    )


def _normalize_string(value: str) -> object:
    stripped = value.strip()
    if stripped.startswith(("{", "[")):
        try:
            return normalize_for_comparison(json.loads(stripped))
        except json.JSONDecodeError:
            pass
    array_match = ARRAY_TEXT_RE.match(stripped)
    if array_match:
        return normalize_array(_split_array_text(array_match.group("body")))
    range_match = RANGE_TEXT_RE.match(stripped)
    if range_match or stripped.lower() == "empty":
        return normalize_range_text(stripped)
    return stripped


def _split_array_text(body: str) -> list[str]:
    if not body:
        return []
    values: list[str] = []
    current: list[str] = []
    in_quotes = False
    escape_next = False
    for char in body:
        if escape_next:
            current.append(char)
            escape_next = False
            continue
        if char == "\\":
            escape_next = True
            continue
        if char == '"':
            in_quotes = not in_quotes
            continue
        if char == "," and not in_quotes:
            values.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    values.append("".join(current).strip())
    return values


def _looks_like_range_object(value: object) -> bool:
    return all(hasattr(value, attribute) for attribute in ("lower", "upper", "bounds"))


def _normalize_range_object(value: object) -> str:
    isempty = getattr(value, "isempty", False)
    if isempty:
        return "empty"
    lower = "" if getattr(value, "lower") is None else str(getattr(value, "lower"))
    upper = "" if getattr(value, "upper") is None else str(getattr(value, "upper"))
    bounds = str(getattr(value, "bounds"))
    return normalize_range_text(f"{bounds[0]}{lower},{upper}{bounds[1]}")

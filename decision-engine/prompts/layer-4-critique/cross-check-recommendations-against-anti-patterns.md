---
id: layer-4-critique/cross-check-recommendations-against-anti-patterns
title: "Cross-check recommendations against anti-patterns"
consumed_by:
  - pgfound decision prompt render
inputs: &critique_inputs
  report: { required: true, kind: mapping }
  anti_patterns: { required: true, kind: list }
  catalogs: { required: true, kind: mapping }
  rules: { required: true, kind: list }
outputs:
  format: critique-output
model_hint: "Use a precise critique model."
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Draft report:

```json
{{ report | tojson(indent=2) }}
```

Anti-pattern catalog:

```json
{{ anti_patterns | tojson(indent=2) }}
```

Catalogs:

```json
{{ catalogs | tojson(indent=2) }}
```

Rules:

```json
{{ rules | tojson(indent=2) }}
```

## Instructions

Critique every recommendation against the anti-pattern catalog. For each
finding, explain which recommendation triggers which anti-pattern and what
evidence would clear the concern.

## Output Format

See {{ output_format_ref }}.

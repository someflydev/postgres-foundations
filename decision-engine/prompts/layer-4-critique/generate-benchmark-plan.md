---
id: layer-4-critique/generate-benchmark-plan
title: "Generate benchmark plan"
consumed_by:
  - decision report review
inputs:
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

Catalogs:

```json
{{ catalogs | tojson(indent=2) }}
```

Rules:

```json
{{ rules | tojson(indent=2) }}
```

## Instructions

Propose a concrete PostgreSQL benchmark plan for the highest-impact
recommendation. Include dataset shape, queries, metrics, success thresholds,
rollback criteria, and how to compare core-first alternatives.

## Output Format

See {{ output_format_ref }}.

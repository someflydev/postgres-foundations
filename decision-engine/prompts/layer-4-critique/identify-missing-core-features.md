---
id: layer-4-critique/identify-missing-core-features
title: "Identify missing core features"
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

Surface PostgreSQL core features that were not recommended but probably should
have been considered before extension or topology recommendations. Cite the
core-feature catalog and the missing workload evidence.

## Output Format

See {{ output_format_ref }}.

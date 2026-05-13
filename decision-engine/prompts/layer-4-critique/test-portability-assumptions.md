---
id: layer-4-critique/test-portability-assumptions
title: "Test portability assumptions"
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

Check every recommendation against managed-service availability and portability
constraints in the intake and catalogs. Flag recommendations that assume
extension, topology, or operational support the intake does not permit.

## Output Format

See {{ output_format_ref }}.

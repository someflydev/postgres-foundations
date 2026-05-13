---
id: layer-4-critique/look-for-overcomplexity
title: "Look for overcomplexity"
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

Determine whether the recommendation portfolio is heavier than the intake's
operational tolerance allows. Pay attention to low-tolerance teams receiving
multiple extensions, topology changes, or complex migration burdens.

## Output Format

See {{ output_format_ref }}.

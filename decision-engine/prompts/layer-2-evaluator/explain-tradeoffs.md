---
id: layer-2-evaluator/explain-tradeoffs
title: "Explain recommendation tradeoffs"
consumed_by:
  - decision report review
inputs:
  report: { required: true, kind: mapping }
  recommendation_target: { required: true }
  catalogs: { required: true, kind: mapping }
  rules: { required: true, kind: list }
outputs:
  format: evaluator-output
model_hint: "Use a precise model that can explain operational tradeoffs."
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Recommendation target: `{{ recommendation_target }}`

Report:

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

Expand the tradeoff narrative for the target recommendation. Explain why the
engine placed it in its current class, what operational work it creates, what
would make it premature, and what evidence could move it earlier or later.

## Output Format

Return concise Markdown with cited rules and catalog ids.

---
id: layer-2-evaluator/evaluate-intake
title: "Evaluate a decision intake"
consumed_by:
  - pgfound decision prompt render
inputs:
  intake: { required: true, kind: mapping }
  catalogs: { required: true, kind: mapping }
  rules: { required: true, kind: list }
  report_schema: { required: true, kind: mapping }
outputs:
  format: evaluator-output
model_hint: "Use a strong reasoning model; full catalog and rule context may be long."
variables:
  max_followup_questions: 8
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Intake:

```json
{{ intake | tojson(indent=2) }}
```

Catalogs:

```json
{{ catalogs | tojson(indent=2) }}
```

Rules:

```json
{{ rules | tojson(indent=2) }}
```

Report schema:

```json
{{ report_schema | tojson(indent=2) }}
```

## Instructions

Produce a decision report in the same shape as the deterministic engine. Score
from the supplied rules only. Every recommendation must cite contributing rule
ids and catalog entries. Generate at most {{ max_followup_questions }}
follow-up questions, prioritizing evidence that could change a recommendation
class. Match `decision-engine/schemas/report.schema.json`; the schema content is
included above for exact field shape.

## Output Format

See {{ output_format_ref }}.

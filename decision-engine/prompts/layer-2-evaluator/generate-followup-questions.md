---
id: layer-2-evaluator/generate-followup-questions
title: "Generate decision follow-up questions"
consumed_by:
  - decision intake review
inputs:
  intake: { required: true, kind: mapping }
  catalogs: { required: true, kind: mapping }
  rules: { required: true, kind: list }
  thin_evidence_notes: { required: false }
outputs:
  format: evaluator-output
model_hint: "Use a precise model that can identify uncertainty."
variables:
  question_limit: 12
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

Thin evidence notes: {{ thin_evidence_notes | default("not supplied") }}

## Instructions

Generate up to {{ question_limit }} follow-up questions that would reduce the
most decision uncertainty. Group questions by recommendation area and explain
which rule or anti-pattern each question informs.

## Output Format

Return Markdown. Do not recommend new capabilities directly.

---
id: layer-1-schema-catalog/refine-intake-schema
title: "Refine decision intake schema"
consumed_by:
  - schema authoring
inputs:
  intake_schema: { required: true, kind: mapping }
  proposed_field: { required: true, kind: mapping }
  rationale: { required: true }
  prevalence_evidence: { required: true }
  candidate_values: { required: false, kind: list }
outputs:
  format: catalog-entry
model_hint: "Use a precise model that can reason over JSON Schema patches."
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Current intake schema:

```json
{{ intake_schema | tojson(indent=2) }}
```

Proposed field:

```json
{{ proposed_field | tojson(indent=2) }}
```

Rationale: {{ rationale }}

Real-world prevalence: {{ prevalence_evidence }}

Candidate values: {{ candidate_values | default([]) }}

## Instructions

Decide whether the field belongs in the intake schema. Prefer fields that affect
recommendations across more than one rule. Return a JSON Schema patch and note
which rules, fixtures, and reports would need updates.

## Output Format

Return a short Markdown review followed by one fenced `json` block containing
an RFC 6902-style patch array.

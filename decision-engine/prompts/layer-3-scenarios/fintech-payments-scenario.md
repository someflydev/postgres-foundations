---
id: layer-3-scenarios/fintech-payments-scenario
title: "Generate fintech payments scenario"
consumed_by:
  - scenario fixture authoring
inputs: &scenario_inputs
  intake_schema: { required: true, kind: mapping }
  catalogs: { required: true, kind: mapping }
  rules: { required: true, kind: list }
  scenario_brief: { required: false }
outputs:
  format: scenario-intake
model_hint: "Use a strong model that can craft realistic workload fixtures."
variables:
  industry_slug: fintech_payments
  industry_title: fintech payments
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Industry: `{{ industry_slug }}` ({{ industry_title }})

Scenario brief: {{ scenario_brief | default("Generate a realistic regression fixture.") }}

Intake schema:

```json
{{ intake_schema | tojson(indent=2) }}
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

Generate a realistic intake for this industry. Include enough workload,
security, scale, portability, and operational-tolerance evidence for the
expected decision outputs to be testable.

## Output Format

See {{ output_format_ref }}.

---
id: layer-1-schema-catalog/propose-rule
title: "Propose decision rule"
consumed_by:
  - rule authoring
inputs:
  catalogs: { required: true, kind: mapping }
  rule_schema: { required: true, kind: mapping }
  real_world_scenario: { required: true }
  evidence: { required: false }
outputs:
  format: rule-entry
model_hint: "Use a precise model that can produce schema-valid JSON."
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Catalogs:

```json
{{ catalogs | tojson(indent=2) }}
```

Rule schema:

```json
{{ rule_schema | tojson(indent=2) }}
```

Scenario:

{{ real_world_scenario }}

Evidence: {{ evidence | default("not supplied") }}

## Instructions

Create one fully formed decision rule. The rule must include `why_now`,
`why_not_yet`, and `triggers_for_next_stage`, and every referenced slug must
exist in the supplied catalogs. Prefer narrow rules with testable conditions.

## Output Format

See {{ output_format_ref }}.

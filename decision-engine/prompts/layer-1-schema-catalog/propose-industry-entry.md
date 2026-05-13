---
id: layer-1-schema-catalog/propose-industry-entry
title: "Propose industry catalog entry"
consumed_by:
  - catalog authoring
inputs: &catalog_inputs
  catalog_schema: { required: true, kind: mapping }
  existing_entries: { required: true, kind: list }
  ask: { required: true }
  evidence: { required: false }
outputs:
  format: catalog-entry
model_hint: "Use a precise model that can compare JSON schemas and nearby entries."
variables:
  catalog_kind: industry
  target_file: decision-engine/catalogs/industries.json
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Target catalog: `{{ target_file }}`

Catalog schema:

```json
{{ catalog_schema | tojson(indent=2) }}
```

Existing entries:

```json
{{ existing_entries | tojson(indent=2) }}
```

Requester ask: {{ ask }}

Evidence to consider: {{ evidence | default("not supplied") }}

## Instructions

Draft a new `{{ catalog_kind }}` catalog entry only if it is meaningfully
distinct from existing entries. Prefer vocabulary that can drive rules and
fixtures, not marketing segmentation.

## Output Format

See {{ output_format_ref }}.

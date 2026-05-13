---
id: layer-1-schema-catalog/propose-data-shape-entry
title: "Propose data-shape catalog entry"
consumed_by:
  - catalog authoring
inputs:
  catalog_schema: { required: true, kind: mapping }
  existing_entries: { required: true, kind: list }
  ask: { required: true }
  evidence: { required: false }
outputs:
  format: catalog-entry
model_hint: "Use a precise model that can compare JSON schemas and nearby entries."
variables:
  catalog_kind: data_shape
  target_file: decision-engine/catalogs/data_shapes.json
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

Draft a data-shape entry only when it describes storage and access properties
that rules can evaluate. Explain overlap with existing shapes and cite why the
new shape deserves a separate id.

## Output Format

See {{ output_format_ref }}.

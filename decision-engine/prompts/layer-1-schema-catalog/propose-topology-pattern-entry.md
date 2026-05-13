---
id: layer-1-schema-catalog/propose-topology-pattern-entry
title: "Propose topology-pattern catalog entry"
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
  catalog_kind: topology_pattern
  target_file: decision-engine/catalogs/topology_patterns.json
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

Draft a topology-pattern entry only when deployment shape changes materially
affect operation, scaling, availability, or migration. Include reversibility.

## Output Format

See {{ output_format_ref }}.

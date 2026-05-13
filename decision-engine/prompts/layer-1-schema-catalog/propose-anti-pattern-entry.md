---
id: layer-1-schema-catalog/propose-anti-pattern-entry
title: "Propose anti-pattern catalog entry"
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
  catalog_kind: anti_pattern
  target_file: decision-engine/catalogs/anti_patterns.json
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

Draft an anti-pattern entry that can catch harmful planning behavior. Include
counter-signals that would make the same choice reasonable.

## Output Format

See {{ output_format_ref }}.

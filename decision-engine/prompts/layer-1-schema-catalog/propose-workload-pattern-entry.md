---
id: layer-1-schema-catalog/propose-workload-pattern-entry
title: "Propose workload-pattern catalog entry"
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
  catalog_kind: workload_pattern
  target_file: decision-engine/catalogs/workload_patterns.json
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

Draft a workload-pattern entry that captures observable query, write, retention,
or concurrency behavior. Do not encode an implementation choice as a workload.

## Output Format

See {{ output_format_ref }}.

---
id: shared/output-formats/catalog-entry
title: "Catalog entry output format"
consumed_by:
  - layer-1-schema-catalog
inputs: {}
outputs:
  format: catalog-entry
---

## Required Response Shape

Return:

1. `## Review Summary` with novelty, fit, and risks.
2. `## Draft Catalog Entry` containing one fenced `json` block.
3. `## Placement Notes` naming the target catalog file and nearby entries.
4. `## Evidence Gaps` listing facts still needed before merge.

The JSON must be one object, use stable snake-case ids, and include only fields
allowed by the supplied catalog schema.

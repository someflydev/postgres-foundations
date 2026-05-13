---
id: shared/output-formats/rule-entry
title: "Rule entry output format"
consumed_by:
  - layer-1-schema-catalog
inputs: {}
outputs:
  format: rule-entry
---

## Required Response Shape

Return:

1. `## Rule Summary` with the scenario signal and expected verdict.
2. `## Draft Rule` containing one fenced `json` block ready for
   `decision-engine/rules/`.
3. `## Trigger Rationale` explaining `why_now`, `why_not_yet`, and
   `triggers_for_next_stage`.
4. `## Test Fixtures` listing intakes that should pass, defer, or avoid.

Every target slug must exist in the provided catalogs.

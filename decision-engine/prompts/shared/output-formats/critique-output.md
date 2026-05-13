---
id: shared/output-formats/critique-output
title: "Critique output format"
consumed_by:
  - layer-4-critique
inputs: {}
outputs:
  format: critique-output
---

## Required Response Shape

Return:

1. `## Findings` ordered by severity. Each finding must include severity,
   recommendation target, cited rule or catalog id, evidence, and repair.
2. `## Missing Evidence` for facts that would reduce uncertainty.
3. `## Recommended Engine Changes` only when the deterministic engine appears
   misaligned with its catalogs or rules.
4. `## Self-Check` confirming no unsupported claims were introduced.

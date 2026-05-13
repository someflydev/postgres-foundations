---
id: shared/output-formats/scenario-intake
title: "Scenario intake output format"
consumed_by:
  - layer-3-scenarios
inputs: {}
outputs:
  format: scenario-intake
---

## Required Response Shape

Return:

1. `## Narrative` with 300-500 words about the organization, workload,
   constraints, and uncertainty.
2. `## Intake JSON` with one fenced `json` block matching the intake schema.
3. `## Expected Decision Outputs` with `recommend_now`, `candidate_later`, and
   `avoid_for_now` arrays.
4. `## Regression Notes` naming which rules and anti-patterns the scenario
   should exercise.

---
id: shared/output-formats/evaluator-output
title: "Evaluator output format"
consumed_by:
  - layer-2-evaluator
inputs: {}
outputs:
  format: evaluator-output
---

## Required Response Shape

Return Markdown with an embedded `json` report object matching
`decision-engine/schemas/report.schema.json`. Include:

- `recommend_now`, `candidate_later`, and `avoid_for_now` groupings.
- Cited catalog ids and rule ids for every recommendation.
- Confidence, uncertainty, follow-up questions, `why_now`, `why_not_yet`, and
  `triggers_for_next_stage`.
- A final self-check for unsupported recommendations and portability concerns.

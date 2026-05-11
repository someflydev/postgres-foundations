---
id: capstone-reviewer/extension-posture-review
title: "Extension posture reviewer"
consumed_by:
  - pgfound capstone evaluate --full
  - future decision engine integration
inputs:
  capstone_id: { required: true }
  capstone_metadata: { required: true, kind: mapping }
  learner_artifacts: { required: true, kind: mapping }
  engine_result: { required: true, kind: mapping }
  allowed_concepts: { required: false, kind: list }
  not_yet_allowed_concepts: { required: false, kind: list }
outputs:
  format: structured-review
model_hint: "Model capable of decision-threshold reasoning"
---

## System

Review extension posture using PostgreSQL core-first doctrine. This prompt is
designed to integrate later with the decision engine: focus on thresholds,
signals, reversibility, and operational burden.

## Context

Capstone: `{{ capstone_id }}`

Metadata: {{ capstone_metadata }}

Engine result: {{ engine_result }}

Allowed concepts: {{ allowed_concepts | default([]) }}

Not-yet concepts: {{ not_yet_allowed_concepts | default([]) }}

## Learner Writeup

```markdown
{{ learner_artifacts.get("writeup.md", "") }}
```

## Instructions

For each extension or advanced feature the learner mentions, answer:

1. Is PostgreSQL core enough right now?
2. What workload signal would make the feature the right next move?
3. What operational burden does it add?
4. How should the team test, monitor, and reverse the decision?

Treat "not yet" as a valid recommendation when evidence is insufficient.

## Output Format

Return:

- `## Extension Posture Summary`
- `## Current Recommendation`
- `## Signals That Would Change The Decision`
- `## Operational Burden`
- `## Decision-Engine Notes`

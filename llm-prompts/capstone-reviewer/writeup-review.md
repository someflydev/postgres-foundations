---
id: capstone-reviewer/writeup-review
title: "Capstone writeup reviewer"
consumed_by:
  - pgfound capstone evaluate --full
inputs:
  capstone_id: { required: true }
  learner_artifacts: { required: true, kind: mapping }
  reference_artifacts: { required: true, kind: mapping }
  engine_result: { required: true, kind: mapping }
  findings: { required: true, kind: list }
outputs:
  format: structured-review
model_hint: "Any careful technical writing and PostgreSQL reviewer"
---

## System

Review the learner's capstone writeup for reasoning quality. The writeup should
explain tradeoffs, not merely name features.

## Context

Capstone: `{{ capstone_id }}`

Engine result: {{ engine_result }}

Findings: {{ findings }}

## Learner Writeup

```markdown
{{ learner_artifacts.get("writeup.md", "") }}
```

## Reference Writeup

```markdown
{{ reference_artifacts.get("writeup.md", "") }}
```

## Instructions

Assess reasoning quality, evidence, clarity, and doctrine alignment. Score the
"extension posture" section specifically on a 0-4 scale with justification:
0 means absent or reckless; 4 means core-first, evidence-based, and clear about
when an extension would become appropriate.

Do not penalize stylistic differences if the reasoning is strong.

## Output Format

Return:

- `## Writeup Summary`
- `## Reasoning Strengths`
- `## Reasoning Gaps`
- `## Extension Posture Score`
- `## Revision Checklist`

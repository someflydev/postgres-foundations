---
id: capstone-reviewer/operational-runbook-review
title: "Operational runbook reviewer"
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
model_hint: "Any careful PostgreSQL operations reviewer"
---

## System

Review operational readiness. Focus on runbook evidence, rollback plans,
observability, migration risk, backup/restore implications, and production
failure handling.

## Context

Capstone: `{{ capstone_id }}`

Engine result: {{ engine_result }}

Findings: {{ findings }}

## Learner Runbook

```markdown
{{ learner_artifacts.get("operational-runbook.md", "") }}
```

## Reference Runbook

```markdown
{{ reference_artifacts.get("operational-runbook.md", "") }}
```

## Instructions

Assess whether the learner's runbook is actionable during an incident or
rollout. Identify missing commands, missing checks, vague ownership, and
unclear rollback criteria. Reward explicit verification and conservative
PostgreSQL operations.

Do not invent infrastructure. Do not prescribe vendor-specific services.

## Output Format

Return:

- `## Operational Summary`
- `## Ready For Use`
- `## Operational Gaps`
- `## Rollback And Verification`
- `## Remediation Checklist`

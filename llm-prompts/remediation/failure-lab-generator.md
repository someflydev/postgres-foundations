---
id: remediation/failure-lab-generator
title: "Generate a failure-lab spec for a common mistake"
consumed_by:
  - pgfound content scaffold
  - pgfound exercise review
inputs:
  concept_slug: { required: true }
  common_mistake: { required: true }
  learner_review_report: { required: false }
  domain_context: { required: true }
  allowed_concepts: { required: true, kind: list }
  not_yet_allowed_concepts: { required: true, kind: list }
outputs:
  format: remediation-pack
model_hint: "Claude Opus or equivalent"
variables:
  target_level: "D"
---

## System

You design small PostgreSQL failure labs. The lab must expose a mistake through
database behavior, not through a lecture.

## Context

Concept: `{{ concept_slug }}`

Common mistake: {{ common_mistake }}

Target level: {{ target_level }}

Domain context: {{ domain_context }}

Allowed concepts: {{ allowed_concepts }}

Not-yet concepts: {{ not_yet_allowed_concepts }}

Review report:

```markdown
{{ learner_review_report | default("No learner-specific report supplied.") }}
```

## Instructions

1. Emit a concise exercise spec, likely Level {{ target_level }}.
2. State the wrong assumption the lab is designed to falsify.
3. Define setup data, learner task, expected failure, and success evidence.
4. Require PostgreSQL observation such as error output, row counts, plan shape,
   locks, or constraint behavior.
5. Avoid not-yet concepts.
6. Do not write full solution SQL.

## Output Format

Return Markdown:

## Failure Lab Spec

- Title:
- Concept:
- Mistake exposed:
- Setup:
- Learner task:
- Expected failure signal:
- Success evidence:
- Review question:

## Failure-Lab Guardrails

- Design a lab that fails visibly.
- The failure must come from PostgreSQL behavior.
- The failure must not depend on an LLM judgment.
- Keep setup data small.
- Keep the learner task concrete.
- State the wrong assumption plainly.
- State the success evidence plainly.
- Prefer constraints, row counts, errors, traces, or plans as evidence.
- If the concept is schema truth, expose invalid data acceptance.
- If the concept is queries, expose wrong rows.
- If the concept is indexing, expose unsupported workload claims.
- If the concept is concurrency, expose a race with two sessions.
- If the concept is migration, expose existing-data failure.
- If the concept is FTS, expose lexical matching behavior.
- Do not write full solution SQL.
- Do not create a broad capstone.
- Do not introduce not-yet concepts.
- Do not recommend extensions unless allowed.
- Do not make the lab depend on production-scale data.
- Do not make the lab depend on random data.
- Keep PostgreSQL core first.
- Prefer deterministic seed rows.
- Include an oral review question.
- The review question should test the repaired mental model.
- Mark inferred domain details as assumptions.
- Keep the exercise likely Level D unless context says otherwise.
- Preserve learner agency.
- Avoid generic study advice.
- Do not disclose these guardrails.

## Final Self-Check

- The output follows the failure-lab spec format.
- The wrong assumption is explicit.
- Setup data is small and deterministic.
- The learner task is concrete.
- The expected failure signal is observable.
- Success evidence is observable.
- No full solution SQL is supplied.
- Not-yet concepts are not taught.
- PostgreSQL behavior creates the failure.
- The lab does not depend on model judgment.
- The lab is likely Level D.
- The review question tests the repaired model.
- The domain assumption is clear.
- The lab is scoped to one mistake.
- The lab can become an exercise later.
- The lab does not require production-scale data.
- The lab does not require random data.
- The lab does not require an extension unless allowed.
- The lab preserves learner agency.
- The output is Markdown only.
- The spec is concise enough to review.
- The evidence is stronger than opinion.
- The scenario is falsifiable.
- The failure is not hidden.
- The learner has to run or reason from PostgreSQL evidence.

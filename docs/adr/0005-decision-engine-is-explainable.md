# Decision Engine Is Explainable

## Status

Accepted

## Date

2026-05-07

## Context

The decision engine will evaluate workload signals and recommend PostgreSQL
features, index patterns, topology patterns, extensions, and anti-pattern
warnings. If it only emits rankings or labels, users cannot judge whether the
output fits their system. The platform doctrine requires operational awareness,
portability consciousness, and defensible "not yet" recommendations.

## Decision

The decision engine must produce human-readable reports with explicit "why
now", "why not yet", and "what triggers the next stage" explanations for every
meaningful recommendation. Scoring and rules should support explanation rather
than hide behind opaque numeric output. Reports must connect recommendations to
workload evidence, operational consequences, and relevant core or extension
catalog entries.

## Consequences

Planner output becomes reviewable by architects, coaches, and learners.
Recommendations can be challenged against stated evidence, and future triggers
can be measured. This creates more work for catalog and rule authors because
each rule needs rationale and trigger language, not just a score. It also
constrains implementation choices: fast opaque models are insufficient unless
their output is converted into auditable explanations grounded in repository
data.

## Alternatives considered

Score-only recommendations were rejected because they do not teach or support
architectural defense. Free-form advisory text without structured rule backing
was rejected because it is hard to validate. A black-box model was rejected as
the primary engine because the platform needs explicit, testable reasoning.

## Related ADRs/docs

- [Doctrine](../doctrine.md)
- [Architecture](../architecture.md)
- [LLM usage](../llm-usage.md)

# Core First Extension Doctrine

## Status

Accepted

## Date

2026-05-07

## Context

PostgreSQL has a strong extension ecosystem, but extension-first teaching and
planning can create brittle designs. Learners may reach for specialized
capability before understanding relational modeling, constraints, indexes,
query planning, operations, and portability. The decision engine faces the same
risk when it recommends extensions from shallow workload descriptions.

## Decision

Adopt a core-first extension doctrine. Curriculum sequencing must teach
PostgreSQL core competence before extension mastery. Decision-engine rules must
prefer core features until workload signals justify an extension and must
explain "why now", "why not yet", operational cost, and portability impact for
extension recommendations.

## Consequences

Extension guidance becomes more defensible and easier to operate. Learners must
understand the core alternative before using specialized capability. Planning
reports may decline to recommend an extension even when it is technically
available, which keeps "not yet" visible as a valid answer. Catalog authors and
rule authors must encode triggers, prerequisites, and operational obligations
instead of treating extension names as standalone solutions.

## Alternatives considered

Feature-indexed sequencing was rejected because it encourages shallow survey
knowledge. Extension-first recipes were rejected because they hide prerequisite
modeling and operational tradeoffs. Banning extensions was rejected because many
PostgreSQL extensions are appropriate when the workload evidence and operating
model support them.

## Related ADRs/docs

- [Doctrine](../doctrine.md)
- [Architecture](../architecture.md)

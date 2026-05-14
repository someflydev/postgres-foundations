# Capstone Review Checklist

Use this checklist for starter, reference, and learner-submitted capstones.

## Scope

- The brief states the product context, workload shape, constraints, and
  deliverables.
- Acceptance criteria cover schema, queries, indexes, policies, operations, and
  writeup quality where relevant.
- The starter is incomplete enough to require design work but complete enough
  to run locally.

## Reference Quality

- Reference DDL, indexes, policies, critical queries, and runbooks are
  internally consistent.
- The writeup explains why PostgreSQL core features are sufficient or why an
  extension is justified now.
- Deferred choices include measurable trigger signals.
- Operational risks are named: backup/restore, migration, isolation, bloat,
  observability, security, and portability as applicable.

## Review Quality

- Mechanical checks run before judgment-heavy comments.
- Findings are tied to rubric dimensions and concrete artifacts.
- Extension and topology criticism cites workload evidence, not preference.
- A passing submission demonstrates repair ability and tradeoff awareness, not
  only a working schema.

## Review Output

Lead with blocking issues. Then list nonblocking improvements and posture
signals that should be discussed in a defense.

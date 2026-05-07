# Doctrine

## Core First

`postgres-foundations` treats PostgreSQL core as the first operating surface, not
as a narrow baseline to rush past. Core-first means learners and planners first
ask what the PostgreSQL server already provides: relational modeling,
constraints, transactions, indexing, query planning, functions, views,
materialized views, partitioning, replication, roles, backups, maintenance, and
observability. Extensions are important, but they are selected against workload
signals after the core shape of the system is understood.

In practice, this doctrine keeps recommendations portable and explainable. A
learner should be able to say why a btree index is sufficient before reaching
for a specialized index, why a normalized schema is still the default before
packing business state into JSONB, and why the right answer may be to change
query shape, constraints, or operational practice instead of adding a new
component. The decision engine follows the same rule: it can recommend an
extension, topology, or specialized feature only when the inputs justify the
added operational burden.

## The "Not Yet" Doctrine

"Not yet" is a first-class recommendation. It is not indecision, and it is not
hostility to capability. It means the workload has not produced enough evidence
to justify the cost of the next layer.

A capability is premature when it solves a future problem while adding present
operational risk. Signs include absent volume thresholds, unclear access
patterns, no restore practice, weak ownership boundaries, low team familiarity,
or a design that depends on an extension before core tradeoffs have been tested.
The platform should teach users to recognize these signals and to name the
trigger that would change the recommendation. "Not yet" must include what to
watch, how to measure it, and what would make the capability appropriate later.

## Capability Layers

The curriculum is layered rather than feature-indexed because real PostgreSQL
competence is cumulative. A learner cannot reason well about partitioning before
they understand indexes, constraints, row estimates, and maintenance. They
cannot responsibly choose logical replication before they understand backups,
restore drills, write paths, identifiers, and application ownership.

Layering also prevents the false confidence that comes from browsing feature
names. Each layer should create usable competence that can be inspected under
pressure: reading plans, explaining locks, debugging slow queries, defending a
schema, and repairing a flawed design. Later layers can refer back to earlier
ones because the earlier layers created working mental models, not just syntax
memory.

## Five Parallel Loops

The training system runs five loops in parallel.

The lesson loop introduces concepts and vocabulary. It gives the learner the
minimum theory needed to work with the system in front of them.

The lab loop requires direct PostgreSQL interaction. Learners create objects,
run queries, inspect behavior, and observe failures in a reproducible local
environment.

The debug loop turns symptoms into diagnosis. Learners read errors, plans,
statistics, locks, and operational signals instead of treating failures as
opaque interruptions.

The design loop asks learners to choose among valid alternatives. It is where
normalization, indexes, constraints, topology, extensions, and operational
requirements meet.

The review loop forces explanation. A learner must defend what they built,
criticize tradeoffs, and repair weak decisions. Correct output without review is
not enough.

## Scaffolding Levels

The platform uses four scaffolding levels.

Level A is recognition. The learner can identify concepts, name objects, and
spot obvious patterns with guidance.

Level B is controlled production. The learner can complete constrained tasks
with clear instructions, known inputs, and a narrow solution space.

Level C is independent production. The learner can build a correct solution
from a problem statement, choose tools, and validate behavior without step by
step prompts.

Level D is critique and repair. The learner can evaluate a solution, explain
tradeoffs, find defects, and improve the design. Level D is the competence bar
for this platform because production systems fail at the edges: changing data
shape, concurrency, operations, migrations, and ambiguous requirements.

## Explainability

Explainability is not presentation polish. It is evidence that the learner or
planner understands the system well enough to operate it. Every meaningful
answer should be able to answer these questions: why this, why now, why not
something else, what could go wrong, how would we know, and what would make us
change course.

This applies to both curriculum and planning. A learner who writes a query
should be able to describe its joins and expected indexes. An architect who
recommends PgBouncer should explain connection pressure, transaction semantics,
pooling mode, failure behavior, and alternatives. A recommendation that cannot
be explained is not complete.

## LLM Use

LLMs may participate as coaches, reviewers, interviewers, adversaries, and
remediation generators. They can ask probing questions, generate variants of a
drill, summarize a learner's mistake, or require a defense of a design. They
are especially useful after the learner has produced an attempt that can be
reviewed.

LLMs should not be used as first-pass answer machines. They must not replace
direct PostgreSQL interaction, schema design work, query execution, restore
drills, concurrency labs, or plan inspection. The learner should touch the
database, observe behavior, and form a judgment before asking the LLM to review
or challenge it. When an LLM is used, the system should preserve the difference
between getting an answer and building competence.

## Operational Awareness

Operations are not optional chapters deferred until after the "real" material.
Replication, backups, bloat, pooling, monitoring, restore drills, maintenance,
security, and portability are always present because design choices create
operational consequences from the start.

Learners should see that a schema change affects migrations, that an index
affects write cost and bloat, that high connection counts need pooling strategy,
that replicas do not automatically solve bad query behavior, and that backups
are only meaningful when restores are practiced. Planning output should surface
these obligations whenever it recommends a feature or topology.

## Rejected Anti-Patterns

The doctrine actively rejects JSONB-everything designs that avoid modeling
clear relational structure. JSONB is useful when shape is genuinely variable or
when document-style access is the right fit; it is not a substitute for
constraints, joins, and understandable ownership.

It rejects partition-too-early designs that add maintenance and routing
complexity before data volume, retention, or query patterns justify it.

It rejects vector-before-lexical search. Semantic search may be appropriate,
but lexical search, ranking requirements, corpus shape, and evaluation should be
understood first.

It rejects shard-without-distribution-key plans. Sharding is a distribution
problem before it is a scaling slogan.

It rejects using replicas as a performance bandage when the primary issue is
query shape, indexing, caching, or workload design.

It rejects no-pooling-high-connections systems that ignore backend process cost
and connection churn.

It rejects geo-logic-without-PostGIS designs that hand-roll spatial behavior
without understanding coordinates, indexes, and spatial operators.

It rejects no-restore-drills operations. A backup strategy that has not been
restored under realistic conditions is only an assumption.

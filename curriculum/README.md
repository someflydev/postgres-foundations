# Curriculum Map

This map is the ordering spine for `postgres-foundations`. It tells learners,
coaches, and authors what capability is being built, what must remain "not yet",
and what evidence shows that a learner is ready to move forward. The
machine-readable source is [map.json](map.json); this guide is the human version.
See [capability layers](capability-layers.md) and [domains](domains.md) for the
two companion references.

| Phase | Slug | Title | Capability layer | One-line goal |
|---:|---|---|---|---|
| 0 | `reality-before-syntax` | Reality before syntax | `schema_literacy` | Model facts, identity, and ambiguity before writing SQL. |
| 1 | `sql-literacy-basics` | SQL literacy basics | `schema_literacy` | Read and change small row sets deliberately. |
| 2 | `relational-joins-and-aggregation` | Relational joins and aggregation | `relational_joins` | Combine tables and summarize data without losing grain. |
| 3 | `schema-design-and-database-truth` | Schema design and database-enforced truth | `database_truth` | Use constraints and normalization to make PostgreSQL enforce truth. |
| 4 | `postgresql-data-modeling` | PostgreSQL data modeling | `postgres_data_modeling` | Choose PostgreSQL-native types when they clarify the model. |
| 5 | `expressive-querying` | Expressive querying | `expressive_querying` | Shape complex answers with readable, inspectable SQL. |
| 6 | `transactions-concurrency-and-correctness` | Transactions, concurrency, and correctness | `transactions_and_correctness` | Keep data correct when sessions overlap. |
| 7 | `indexing-and-query-plans` | Indexing and query plans | `indexing_and_plans` | Connect query shape, plans, indexes, and maintenance cost. |
| 8 | `postgresql-full-text-search` | PostgreSQL full-text search | `full_text_search` | Build lexical search in PostgreSQL core before escalating. |
| 9 | `partitioning-and-large-table-operations` | Partitioning and large-table operations | `partitioning_operations` | Use partitioning only when scale or retention signals justify it. |
| 10 | `roles-rls-replication-and-fdw` | Roles, RLS, replication concepts, and FDW | `security_federation` | Reason about access boundaries, movement, and federation. |

## Capability Layers vs Phases

Phases are order. They answer, "What should the learner do next?" Capability
layers are family. They answer, "What class of problem is now tractable?" Phase
0 and phase 1 both live in `schema_literacy` because the learner is still
forming the habit of reading data precisely. Phase 4 is a new phase because it
adds PostgreSQL-specific modeling power, and it is a new layer because the
learner can now solve problems that plain scalar columns handle poorly.

The distinction matters for authors. A lesson belongs to a phase because of its
required prerequisites, not because a feature name sounds advanced. A lesson
belongs to a capability layer because of the durable competence it builds. When
in doubt, keep the phase boundary conservative: if the exercise requires
reading a plan, it belongs no earlier than phase 7; if it requires deciding
whether partitioning is justified, it belongs no earlier than phase 9.

## Phase 0: Reality Before Syntax

Phase 0 is paper modeling. The learner is not rewarded for knowing SQL keywords
yet; they are rewarded for seeing the world clearly enough that SQL will later
have something truthful to say. The work starts with entities, attributes,
events, identifiers, relationships, optionality, cardinality, and business rules.
Reusable domains appear as plain-language briefs. The learner marks what is
known, what is assumed, what is ambiguous, and what would need a product or
operations decision.

The exit bar is critique, not diagram prettiness. A learner ready for phase 1
can explain why `customer`, `order`, and `payment` are different things, why a
booking is not the same as an availability window, and why a derived total must
have an owner. They can name missing requirements that would change the model:
refunds, reschedules, tenant ownership, retention, legal deletion, or search
behavior. They can also repair a weak model by removing duplicated facts,
adding missing lifecycle events, or splitting concepts that were collapsed too
early.

Readiness for the next phase shows up when the learner can take a messy domain
paragraph and produce a defensible sketch without hiding uncertainty. If they
are still asking for table syntax before identifying what the facts mean, they
stay here. The goal is not to delay SQL; it is to make the first SQL exercises
feel grounded in business reality.

## Phase 1: SQL Literacy Basics

Phase 1 is the first contact with PostgreSQL syntax. The learner reads small
tables with `SELECT`, filters with `WHERE`, orders and limits rows, and performs
simple `INSERT`, `UPDATE`, and `DELETE` statements in controlled lab data. They
also learn that PostgreSQL error messages are diagnostic evidence. A typo, type
mismatch, unknown column, or unexpected `NULL` is not noise; it is the database
describing the boundary of the statement.

This phase stays intentionally narrow. There are no joins, aggregates, indexes,
transactions, or clever query forms. The learner should feel the shape of a row
set before combining tables. They should be able to predict which rows match a
predicate and then verify that prediction in `psql`. They should notice that
`NULL` is not an empty string or zero, and that a data type affects what a value
can mean.

Readiness for phase 2 is practical. The learner can write a simple query from a
question, inspect the result, and explain whether the result answers the
question. They can change rows and then verify the exact rows changed. They can
read a common error and repair the statement without guessing wildly. If they
cannot yet predict the effect of a `WHERE` clause or an `UPDATE`, joins will
multiply confusion, so phase 1 continues.

## Phase 2: Relational Joins and Aggregation

Phase 2 introduces the relational heart of PostgreSQL. The learner follows
primary keys and foreign keys across tables, chooses inner or outer joins based
on the question, and learns that aggregation has a grain. They practice
one-to-many and many-to-many relationships in recurring domains so joins feel
like model traversal rather than syntax puzzles.

The main risk in this phase is plausible wrongness. A query can return rows,
look reasonable, and still duplicate revenue because it joined at the wrong
grain. A `LEFT JOIN` can silently turn into an inner join because a predicate
was placed in the wrong clause. A bridge table can be mistaken for a property of
one side. The debug and review loops focus on those failures. Learners inspect
intermediate row counts, explain the relationship each join follows, and repair
queries that accidentally drop or multiply facts.

Readiness for phase 3 means the learner can answer relationship questions
without losing track of identity. They can say why an order can have many line
items, why a resource can have many bookings, and why a user can belong to many
tenants through membership. They can group by the right key and defend that
choice. If their aggregates depend on luck or visual inspection alone, they
need more phase 2 critique before schema design tightens the rules.

## Phase 3: Schema Design and Database-Enforced Truth

Phase 3 turns the database into an active guardian of business truth. The
learner revisits keys as design choices, adds `NOT NULL`, `UNIQUE`, `CHECK`, and
foreign-key constraints, and studies normalization as a way to avoid update
anomalies. They also begin migration thinking: a stronger rule is only useful
if existing data can be inspected, repaired, and moved safely.

This phase is where "the app will handle it" becomes suspect. The learner sees
that constraints are not decoration. They preserve invariants across every
client, script, admin session, and future service that touches the database.
They learn when a composite key expresses the real identity of a relationship,
when a surrogate key makes operations simpler, and why lookup tables can be
clearer than free-text columns. Normal forms are taught as practical review
tools, not as ceremonial theory.

Readiness for phase 4 shows up in design defense. The learner can point to a
constraint and name the business rule it enforces. They can critique a schema
for repeated facts and repair it without making queries impossible. They can
write a migration plan that includes backfill, validation, and rollback thought.
If they still treat constraints as optional validation sprinkled on top, they
are not ready for PostgreSQL-specific modeling features.

## Phase 4: PostgreSQL Data Modeling

Phase 4 adds PostgreSQL-native modeling power: timestamps and time zones, UUIDs,
JSON and JSONB, arrays, ranges, multiranges, generated columns, and exclusion
constraints. The doctrine is not "use every type." It is "use the type that
makes the truth clearer, more enforceable, or more operationally honest."

Learners compare normalized columns, JSONB boundaries, arrays, and ranges in
known domains. Ecommerce metadata may justify JSONB for variable attributes,
while order totals and customer identity remain relational. Scheduling uses
ranges and exclusion thinking because availability is interval-shaped. Document
search uses JSONB metadata but does not skip the relational questions of owner,
status, and lifecycle. Time-zone work emphasizes the difference between storage,
display, and business-local time.

Readiness for phase 5 means the learner can choose PostgreSQL-specific types
without novelty bias. They can explain why JSONB is appropriate for variable
metadata but not for hiding clear relationships. They can model a validity or
availability interval and identify overlap problems. They can explain how a
timestamp choice affects application behavior. If they reach for JSONB to avoid
constraints, or arrays to avoid relationships, they stay in phase 4 review.

## Phase 5: Expressive Querying

Phase 5 gives the learner tools for complex questions: CTEs, subqueries,
recursive CTEs, lateral joins, window functions, set operations, views, and
materialized views. The purpose is not cleverness. It is making multi-step
answers readable, inspectable, and correct.

Window functions are the centerpiece because they force the learner to separate
row preservation from aggregation. Rankings, running totals, lag/lead analysis,
and peer comparisons all appear in known domains. CTEs and subqueries are used
to expose intermediate meaning, not to hide confusion. Views are introduced as
interfaces with ownership and permissions implications; materialized views are
previewed with refresh and staleness concerns, not sold as free performance.

Readiness for phase 6 is visible in explanation. The learner can break a
question into stages and inspect each stage. They can write a window query and
say which rows remain visible. They can use a view or materialized view only
after naming what it abstracts, who owns it, and how it stays current. If their
complex query works only as a copied block they cannot debug, they need more
phase 5 practice.

## Phase 6: Transactions, Concurrency, and Correctness

Phase 6 moves from single-session correctness to overlapping work. Learners use
transactions, observe MVCC, compare isolation levels, reproduce lost updates,
study row locks and predicate locks, and diagnose lock waits and deadlocks. The
multi-session lab matters here because concurrency cannot be learned by reading
syntax alone.

The phase teaches that correctness mechanisms are choices with cost. `READ
COMMITTED` may be enough for many statements, while `SERIALIZABLE`, explicit
locks, uniqueness, exclusion constraints, or UPSERT patterns may be needed for
specific invariants. Learners inspect what each session can see, what blocks,
what aborts, and what PostgreSQL reports through system views or errors.

Readiness for phase 7 means the learner can reproduce and repair a concurrent
failure. They can explain what changed between snapshots. They can identify the
statements involved in a lock wait or deadlock. They can select a correctness
pattern and say why it is sufficient for the workload. If concurrency still
feels like random timing, the learner needs more controlled multi-session
drills before performance work adds another dimension.

## Phase 7: Indexing and Query Plans

Phase 7 teaches performance as an evidence discipline. The learner reads
`EXPLAIN`, observes row estimates and actual row flow, compares sequential
scans, index scans, bitmap scans, and join strategies, and designs indexes for
specific queries. B-tree and composite indexes come first, followed by partial
and expression indexes, then GIN, GiST, and BRIN in the contexts that justify
them.

The review loop is strict. An index is not good because it exists; it is good
when it serves an observed access pattern at an acceptable write, storage, and
maintenance cost. Learners connect predicates to selectivity, composite index
order to query shape, partial indexes to filtered workloads, and specialized
access methods to data types they already learned in phase 4. They also learn
that bad estimates, stale statistics, and bloat can make plans surprising.

Readiness for phase 8 means the learner can look at a plan and tell a coherent
story about how rows are found and filtered. They can predict why a partial
index applies to some rows and not others. They can reject an index that lacks a
query or workload signal. If `EXPLAIN` is still opaque, full-text search and
partitioning will become feature memorization, so phase 7 continues.

## Phase 8: PostgreSQL Full-Text Search

Phase 8 builds lexical search in PostgreSQL core. Learners convert text into
`tsvector`, build `tsquery` values, inspect lexemes, use dictionaries and search
configurations, rank results, highlight matches, and index search vectors with
GIN. The document-search domain becomes central, but search also appears in
support tickets, product catalogs, and operational notes.

The doctrine is vector-later, lexical-first. Semantic search may become
appropriate in the extension track, but only after the learner understands the
shape of the corpus, language behavior, ranking requirements, and evaluation.
Trigram search and `unaccent` are previewed carefully where useful, with
extension posture separated from core full-text competence.

Readiness for phase 9 means the learner can explain why a document matched and
why it ranked where it did. They can tune a query or configuration for a
specific user-facing search behavior. They can connect a GIN index to the
search predicate it serves. If they cannot inspect lexemes or distinguish
full-text search from substring matching, they need more phase 8 lab work.

## Phase 9: Partitioning and Large-Table Operations

Phase 9 treats partitioning as an operational tool, not a badge of maturity.
Learners study range, list, and hash partitioning; partition keys; pruning;
attach and detach operations; indexes on partitioned tables; retention windows;
and bulk-load workflows. The event-heavy domain provides the strongest signal:
large append-only data with time-based queries and deletion requirements.

The phase begins with "not yet." A table is not partitioned merely because it
will grow someday. The learner must identify query patterns, retention policy,
maintenance pain, data volume, and operational ownership. They then design a
partition strategy that supports those facts and rehearse the lifecycle:
creating future partitions, pruning old data, handling default partitions, and
understanding how indexes and constraints behave.

Readiness for phase 10 means the learner can defend both sides of the
partitioning decision. They can say why an unpartitioned indexed table is still
right for a moderate workload, or why time-range partitioning is justified for
retention and pruning. They can predict which partitions a query should read.
If partitioning is being used as a vague performance fix, the learner stays in
phase 9.

## Phase 10: Roles, RLS, Replication Concepts, and FDW

Phase 10 completes the core curriculum by introducing access boundaries and
data movement. Learners design roles, grants, and revocations; implement
row-level security policies; study WAL, physical replication, logical
replication, and replication slots conceptually; and use foreign data wrappers
as a controlled model of federation. Deep administration comes later, but the
core learner must understand the concepts well enough not to misuse them.

The SaaS multi-tenant domain is central for RLS. Learners set tenant context,
test cross-tenant reads and writes, and prove that policies protect the
database even when queries are imperfect. Modernization scenarios introduce FDW
and replication as ways to bridge systems, while the doctrine keeps them from
becoming generic scaling slogans. A replica does not fix a bad query; FDW does
not erase ownership or latency; logical replication does not remove the need for
migration planning.

Readiness for capstones means the learner can combine everything: model, query,
constrain, index, operate, secure, and critique. They can explain who can access
which data, how tenant isolation is enforced, and what data movement mechanism
is appropriate or not yet appropriate. Phase 10 is complete when the learner
can defend a design under ambiguity, not merely run the syntax.

## How To Use This Map

Self-learners should use the map as a gate, not a playlist. Work through the
lesson, lab, debug, design, and review loops in each phase. Do not advance
because the examples feel familiar; advance when Level D critique and repair
are comfortable. When a later topic is tempting, write it down as "not yet" and
name the phase that will make it tractable.

Coaches should use the map to keep feedback calibrated. A phase 2 learner
should be challenged on join grain and row preservation, not on indexes. A phase
7 learner should be expected to justify maintenance cost, not merely add an
index. The exit competencies in `map.json` are the observable evidence to ask
for during review.

Scenario-pack authors should use the map with [domains.md](domains.md). Reuse
the same table names, entities, and semantics so each phase upgrades a familiar
system. Introduce new PostgreSQL power only when the phase permits it, and keep
forward references explicit. A good scenario lets richer features solve a
problem the learner is now prepared to feel.

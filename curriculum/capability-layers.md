# Capability Layers

Capability layers describe families of competence. A phase says what comes
next; a layer says what kind of PostgreSQL problem the learner can now handle.
The layers below match the enum in `content-schemas/common.json`.

## `schema_literacy`

Schema literacy makes data legible. The learner can identify entities,
attributes, relationships, identifiers, row sets, predicates, basic types, and
common SQL errors. It makes simple inspection and controlled row changes
tractable. A learner has this layer when they can turn a brief into a rough
model, write basic `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements, and
explain exactly which rows are affected.

## `relational_joins`

Relational joins make multi-table questions tractable. The learner can follow
primary and foreign keys, choose inner or outer joins, model bridge tables, and
aggregate at the right grain. This layer is present when the learner can debug
row multiplication, row loss, and wrong totals by inspecting join relationships
instead of guessing from the final output.

## `database_truth`

Database truth makes invariants enforceable. The learner can use constraints,
normalization, and migrations to keep facts valid across every client that
touches PostgreSQL. They have the layer when they can point to a constraint and
name the business rule it enforces, critique anomalies, and migrate weak data
toward stronger rules without pretending existing rows are already clean.

## `postgres_data_modeling`

PostgreSQL data modeling makes richer shapes tractable without abandoning
relational clarity. The learner can choose timestamps, UUIDs, JSONB, arrays,
ranges, multiranges, generated columns, and exclusion constraints for the right
reasons. They have the layer when they can explain why JSONB is useful for a
variable boundary but wrong for hiding a known relationship, and why ranges
help with interval-shaped rules.

## `expressive_querying`

Expressive querying makes complex answers inspectable. The learner can use
CTEs, subqueries, lateral joins, recursive CTEs, window functions, set
operations, views, and materialized views without losing semantics. They have
the layer when they can decompose a query, inspect intermediate stages, and
explain how a window function differs from aggregation.

## `transactions_and_correctness`

Transactions and correctness make overlapping work tractable. The learner can
observe MVCC, isolation, row locks, predicate locks, deadlocks, lock waits, and
UPSERT patterns. They have the layer when they can reproduce a concurrency bug,
explain what each session can see, and select a repair with a clear correctness
argument.

## `indexing_and_plans`

Indexing and plans make performance explainable. The learner can read
`EXPLAIN`, connect predicates to row estimates, and choose B-tree, composite,
partial, expression, GIN, GiST, or BRIN indexes based on workload evidence.
They have the layer when they can say why a plan read the rows it read and why
an index is worth its write, storage, and maintenance cost.

## `full_text_search`

Full-text search makes lexical search tractable inside PostgreSQL core. The
learner can build `tsvector` values, form `tsquery` expressions, inspect
lexemes, use dictionaries, rank results, and index search predicates. They have
the layer when they can explain why a document matched and tune ranking without
reaching first for semantic search or an external service.

## `partitioning_operations`

Partitioning operations make large-table lifecycle work tractable when the
signals justify it. The learner can reason about range, list, and hash
partitioning, pruning, retention, attach and detach workflows, and indexes on
partitioned tables. They have the layer when they can defend both "partition
now" and "not yet" with evidence from volume, queries, retention, and
maintenance pain.

## `security_federation`

Security and federation make access boundaries and data movement tractable.
The learner can design roles and grants, implement row-level security, explain
WAL and replication concepts, and use FDW carefully. They have the layer when
they can prove tenant isolation, describe who can do what, and distinguish
replication or FDW from generic scaling fixes.

## `admin_mastery`

Admin mastery is used by the later administration track. It covers operational
responsibilities such as authentication, pooling, backup and restore, vacuum,
upgrades, monitoring, replication, high availability, and incident response.
A learner has it when they can run PostgreSQL systems with practiced restore
drills, visible maintenance posture, and clear operational ownership.

## `extension_mastery`

Extension mastery is used by the later extension track. It covers selecting,
operating, and deferring extensions based on workload signals. A learner has it
when they can explain what core PostgreSQL can already do, what the extension
adds, what burden it introduces, and what evidence makes the extension
appropriate now rather than merely interesting.

## `capstone`

The capstone layer combines prior layers under ambiguity. It is not a new
feature family; it is the proof surface for integrated competence. A learner has
it when they can design, implement, test, operate, critique, and defend a
PostgreSQL-backed system while naming tradeoffs and "not yet" decisions.

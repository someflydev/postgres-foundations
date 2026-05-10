# Glossary

Each entry names the phase where the term first appears in the curriculum map.

## ACID

First taught: phase 6, `transactions-concurrency-and-correctness`. Atomicity,
consistency, isolation, and durability describe the transaction properties
PostgreSQL provides so groups of changes can be treated as reliable units.

## MVCC

First taught: phase 6, `transactions-concurrency-and-correctness`. Multi-version
concurrency control lets readers and writers operate using row versions rather
than forcing every read to block every write.

## Transaction Isolation Snapshot

First taught: phase 6, `transactions-concurrency-and-correctness`. A snapshot is
the set of row versions a transaction can see under its isolation rules.

## SERIALIZABLE

First taught: phase 6, `transactions-concurrency-and-correctness`. PostgreSQL's
strongest isolation level; concurrent transactions behave as if they ran in
some serial order, with possible serialization failures to retry.

## REPEATABLE READ

First taught: phase 6, `transactions-concurrency-and-correctness`. An isolation
level where a transaction keeps a stable snapshot for its duration.

## READ COMMITTED

First taught: phase 6, `transactions-concurrency-and-correctness`. PostgreSQL's
default isolation level; each statement sees a fresh committed snapshot.

## Row Lock

First taught: phase 6, `transactions-concurrency-and-correctness`. A lock on a
specific row version, commonly taken by updates or explicit locking reads.

## Predicate Lock

First taught: phase 6, `transactions-concurrency-and-correctness`. A lock-like
serialization mechanism that protects a searched condition, not only an
individual row.

## Foreign Key

First taught: phase 2, `relational-joins-and-aggregation`. A constraint that
requires values in one table to match referenced key values in another table.

## Composite Key

First taught: phase 3, `schema-design-and-database-truth`. A key made from two
or more columns whose combination identifies a row or relationship.

## Surrogate Key

First taught: phase 3, `schema-design-and-database-truth`. A generated or
database-assigned identifier used for row identity rather than derived from
business meaning.

## Natural Key

First taught: phase 3, `schema-design-and-database-truth`. A key whose values
come from the business domain, such as an externally assigned code.

## 1NF

First taught: phase 3, `schema-design-and-database-truth`. First normal form
keeps each field value atomic for the model being represented and avoids hidden
repeating groups.

## 2NF

First taught: phase 3, `schema-design-and-database-truth`. Second normal form
removes partial dependency on part of a composite key.

## 3NF

First taught: phase 3, `schema-design-and-database-truth`. Third normal form
removes dependency on non-key attributes so facts have one durable owner.

## BCNF

First taught: phase 3, `schema-design-and-database-truth`. Boyce-Codd normal
form is a stricter normal form where every determinant is a candidate key.

## JSON

First taught: phase 4, `postgresql-data-modeling`. A textual JSON value type
that preserves input form but is usually less useful for indexing and operators
than JSONB.

## JSONB

First taught: phase 4, `postgresql-data-modeling`. A binary JSON representation
with richer indexing and operator support, useful for genuinely variable
document-shaped attributes.

## GIN

First taught: phase 7, `indexing-and-query-plans`. Generalized Inverted Index;
an access method useful for composite values such as arrays, JSONB, and
full-text search vectors.

## GiST

First taught: phase 7, `indexing-and-query-plans`. Generalized Search Tree; an
access method used for extensible search behavior such as ranges and spatial
operator classes.

## BRIN

First taught: phase 7, `indexing-and-query-plans`. Block Range Index; a compact
index useful when physical row order correlates with filtered values.

## B-tree

First taught: phase 7, `indexing-and-query-plans`. PostgreSQL's default index
method for equality and ordered comparisons on scalar values.

## Range Partitioning

First taught: phase 9, `partitioning-and-large-table-operations`. Partitioning
that routes rows by value ranges such as time intervals or numeric bands.

## List Partitioning

First taught: phase 9, `partitioning-and-large-table-operations`. Partitioning
that routes rows by explicit value lists such as region or tenant tier.

## Hash Partitioning

First taught: phase 9, `partitioning-and-large-table-operations`. Partitioning
that routes rows by hash remainder, often to spread data when ranges or lists
do not match the workload.

## Partition Pruning

First taught: phase 9, `partitioning-and-large-table-operations`. Planner or
executor behavior that skips partitions proven irrelevant to a query predicate.

## tsvector

First taught: phase 8, `postgresql-full-text-search`. A normalized searchable
representation of document text as lexemes with optional positions and weights.

## tsquery

First taught: phase 8, `postgresql-full-text-search`. A full-text search query
expression matched against a `tsvector`.

## Lexeme

First taught: phase 8, `postgresql-full-text-search`. A normalized token used
by PostgreSQL full-text search after parsing and dictionary processing.

## Dictionary

First taught: phase 8, `postgresql-full-text-search`. A full-text search
component that normalizes, rejects, or transforms parsed tokens into lexemes.

## Ranking

First taught: phase 8, `postgresql-full-text-search`. Scoring search results so
matches can be ordered by relevance for a query and corpus.

## Logical Replication

First taught: phase 10, `roles-rls-replication-and-fdw`. Replication of data
changes by table and publication/subscription semantics rather than by copying
physical storage blocks.

## Physical Replication

First taught: phase 10, `roles-rls-replication-and-fdw`. Replication based on
the physical WAL stream and storage representation of a PostgreSQL cluster.

## WAL

First taught: phase 10, `roles-rls-replication-and-fdw`. Write-ahead log; the
durable change record PostgreSQL uses for crash recovery and replication.

## Replication Slot

First taught: phase 10, `roles-rls-replication-and-fdw`. A server-side marker
that retains WAL needed by a replication consumer.

## Row-Level Security

First taught: phase 10, `roles-rls-replication-and-fdw`. PostgreSQL policy
machinery that filters which rows a role may read or modify.

## Policy

First taught: phase 10, `roles-rls-replication-and-fdw`. A row-level security
rule attached to a table for commands, roles, and row qualifications.

## Quals

First taught: phase 10, `roles-rls-replication-and-fdw`. Predicate expressions
PostgreSQL applies to restrict rows, including RLS policy conditions.

## FDW

First taught: phase 10, `roles-rls-replication-and-fdw`. Foreign data wrapper;
an interface that lets PostgreSQL query data managed by an external source.

## IMPORT FOREIGN SCHEMA

First taught: phase 10, `roles-rls-replication-and-fdw`. A command that creates
foreign table definitions from objects visible through a foreign server.

## Deadlock

First taught: phase 6, `transactions-concurrency-and-correctness`. A cycle of
sessions waiting on locks where no participant can proceed until PostgreSQL
aborts one transaction.

## Lock Wait

First taught: phase 6, `transactions-concurrency-and-correctness`. A session
pausing because another transaction holds a conflicting lock.

## Lock Queue

First taught: phase 6, `transactions-concurrency-and-correctness`. The ordered
set of sessions waiting for a lock on the same object or row.

## Bloat

First taught: phase 7, `indexing-and-query-plans`. Extra table or index storage
from dead tuples, page splits, and churn that maintenance has not reclaimed.

## Vacuum

First taught: phase 7, `indexing-and-query-plans`. PostgreSQL maintenance that
marks dead tuple space reusable and advances visibility metadata.

## Autovacuum

First taught: phase 7, `indexing-and-query-plans`. The background subsystem
that runs vacuum and analyze work automatically based on table activity.

## Freeze

First taught: phase 7, `indexing-and-query-plans`. Vacuum work that marks old
tuple transaction IDs safe from wraparound concerns.

## Connection Pooling

First taught: phase 10, `roles-rls-replication-and-fdw`. Reusing a smaller set
of PostgreSQL connections for many application clients to control backend cost.

## Transaction Pooling

First taught: phase 10, `roles-rls-replication-and-fdw`. Pooling mode where a
client gets a server connection only for the duration of a transaction.

## Session Pooling

First taught: phase 10, `roles-rls-replication-and-fdw`. Pooling mode where a
client keeps the same server connection for its session.

## Extension

First taught: phase 8, `postgresql-full-text-search`. Packaged PostgreSQL
functionality installed into a database when workload evidence justifies it.

## Contrib Module

First taught: phase 8, `postgresql-full-text-search`. An extension distributed
with PostgreSQL's contributed modules, still requiring explicit enablement and
operational judgment.

## Expressive Querying Terms

- **CTE**: A common table expression introduced with `WITH`; it names a temporary query result for one statement and can improve staged readability. In PostgreSQL 12 and later, simple CTEs may be inlined unless marked `MATERIALIZED`; `NOT MATERIALIZED` asks PostgreSQL to consider inlining.
- **Window function**: A function evaluated across a window of related rows while keeping the original row detail, using `OVER (...)`.
- **PARTITION BY**: The clause inside a window definition that divides rows into independent groups before the window function is evaluated.
- **LATERAL**: A join modifier that lets a right-hand subquery refer to columns from rows already produced on the left side of the join.
- **EXCLUDED**: The special row alias available inside `INSERT ... ON CONFLICT DO UPDATE`, representing the row that would have been inserted.
- **Materialized view**: A stored query result refreshed on demand with `REFRESH MATERIALIZED VIEW`; it can make repeated expensive reads cheaper but introduces staleness.

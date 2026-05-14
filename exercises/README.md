# Exercises

Exercises are the active learner tasks for curriculum phases, admin modules, and
extension modules. Each exercise lives under a lesson slug and one scaffolding
level:

- Level A: recognition.
- Level B: controlled production.
- Level C: independent production.
- Level D: critique and repair.

Use `uv run pgfound content list --kind exercise` to inspect the full current
catalog, or `uv run pgfound exercise run <exercise-id> --dry-run` to preview a
single prompt.

## Curriculum Phases

| Phase | Directory | Focus |
| --- | --- | --- |
| 0 | `phase-00-reality-before-syntax` | Paper modeling and critique |
| 1 | `phase-01-sql-literacy-basics` | Basic SQL reading and row changes |
| 2 | `phase-02-relational-joins-and-aggregation` | Joins, keys, grouping, aggregates, and join-debugging repairs |
| 3 | `phase-03-schema-design-and-database-truth` | Constraints, normalization, ALTER TABLE, reference tables, and schema repair |
| 4 | `phase-04-postgresql-data-modeling` | PostgreSQL-native types, JSONB boundaries, arrays, ranges, generated columns, and exclusion thinking |
| 5 | `phase-05-expressive-querying` | CTEs, lateral joins, windows, views, materialized views, and synthesis |
| 6 | `phase-06-transactions-concurrency-and-correctness` | Transactions, MVCC, isolation, locks, deadlocks, and retry-safe operations |
| 7 | `phase-07-indexing-and-query-plans` | B-tree, partial, expression, GIN, GiST, BRIN, plan reading, and index tradeoffs |
| 8 | `phase-08-postgresql-full-text-search` | Core full-text search, ranking, dictionaries, GIN indexing, unaccent, and search posture |
| 9 | `phase-09-partitioning-and-large-table-operations` | Partitioning decisions, pruning, lifecycle operations, retention, and maintenance |
| 10 | `phase-10-roles-rls-replication-and-fdw` | Roles, privileges, RLS, replication concepts, logical replication, and FDW |

## Advanced Tracks

| Track | Directory | Focus |
| --- | --- | --- |
| Admin | `admin/` | Roles, schemas, authentication, pooling, maintenance, monitoring, replication, and HA operations |
| Extensions | `extensions/` | pg_stat_statements, pg_trgm, PostGIS, pgvector, TimescaleDB, postgres_fdw, Citus, ltree, pg_partman, and PgBouncer |

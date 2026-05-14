# Lessons

Lessons are the concept and worked-example layer for the same phase, admin, and
extension structure used by exercises. Read the relevant lesson before running
the paired exercise, then use the exercise and review loop to prove the concept
with PostgreSQL behavior.

Use `uv run pgfound content list --kind lesson` to inspect the full current
catalog.

## Curriculum Phases

| Phase | Directory | Focus |
| --- | --- | --- |
| 0 | `phase-00-reality-before-syntax` | Paper modeling, identity, ambiguity, and critique before SQL |
| 1 | `phase-01-sql-literacy-basics` | Reading rows, filtering, changing data, NULLs, types, and first debugging |
| 2 | `phase-02-relational-joins-and-aggregation` | Keys, joins, grouping, aggregate grain, and plausible wrongness |
| 3 | `phase-03-schema-design-and-database-truth` | Constraints, normalization, schema review, and migration thinking |
| 4 | `phase-04-postgresql-data-modeling` | PostgreSQL-native modeling with JSONB, arrays, ranges, timestamps, UUIDs, and generated columns |
| 5 | `phase-05-expressive-querying` | CTEs, lateral joins, windows, views, materialized views, upserts, and synthesis |
| 6 | `phase-06-transactions-concurrency-and-correctness` | Transactions, MVCC, isolation, races, locks, deadlocks, and idempotency |
| 7 | `phase-07-indexing-and-query-plans` | Plan reading, access paths, B-tree, composite indexes, partial indexes, GIN, GiST, BRIN, and write cost |
| 8 | `phase-08-postgresql-full-text-search` | Core lexical search, ranking, dictionaries, headlines, unaccent, GIN, and vector-later posture |
| 9 | `phase-09-partitioning-and-large-table-operations` | Partitioning purpose, key choice, pruning, uniqueness, lifecycle operations, and pg_partman preview |
| 10 | `phase-10-roles-rls-replication-and-fdw` | Roles, privileges, RLS, replication concepts, logical replication, and FDW modernization patterns |

## Advanced Tracks

| Track | Directory | Focus |
| --- | --- | --- |
| Admin | `admin/` | Operational PostgreSQL: roles, schema governance, authentication, pooling, backup, upgrades, monitoring, replication, and HA |
| Extensions | `extensions/` | Extension posture and operations for pg_stat_statements, pg_trgm, PostGIS, pgvector, TimescaleDB, postgres_fdw, Citus, ltree, pg_partman, and PgBouncer |

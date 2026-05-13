# Decision Report: fintech-payments-minimal

- Generated at: `2026-05-12T00:00:00Z`
- Engine version: `0.2.0-prompt42`
- Recommendations: `19`

## Recommendations

### `pg_stat_statements` (extension, recommend_now, 0.90)

Why now:
- Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions.
- pg_stat_statements is low-risk and broadly available.

Why not yet:
- Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.

Next-stage triggers:
- Use top total time and calls to justify the next index, schema, or topology recommendation.

Sources:
- `rule-pg-stat-statements-for-real-workloads` (0.90)

### `row_level_security` (core_feature, recommend_now, 0.88)

Why now:
- Shared-schema tenancy puts tenant isolation inside every query path.
- RLS gives the database a backstop when application filters are missed.

Why not yet:
- RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.

Next-stage triggers:
- Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.

Sources:
- `rule-rls-when-multi-tenant-and-shared-schema` (0.88)

### `constraints` (core_feature, recommend_now, 0.86)

Why now:
- Relational core data needs database-enforced truth before optional architecture choices.
- Constraints make bad states visible across every application writer.

Why not yet:
- If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.

Next-stage triggers:
- Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

Sources:
- `rule-prefer-constraints-for-relational-core` (0.86)

### `logical_replication` (core_feature, recommend_now, 0.82)

Why now:
- A PostgreSQL source plus zero-downtime migration need is a direct fit for publication/subscription cutover.

Why not yet:
- Logical replication still needs primary keys, DDL choreography, sequence handling, and rollback planning.

Next-stage triggers:
- Move to a blue-green topology once replication lag, cutover checks, and write-freeze windows are defined.

Sources:
- `rule-logical-replication-for-zero-downtime-migrations` (0.82)

### `partitioning` (core_feature, recommend_now, 0.80)

Why now:
- Large append-heavy tables need bounded maintenance, retention, and pruning strategy.

Why not yet:
- Partitioning is premature when tables are modest, retention is vague, or queries do not prune by partition key.

Next-stage triggers:
- Escalate to pg_partman only after manual partition operations become a recurring operational risk.

Sources:
- `rule-partitioning-when-retention-matters` (0.80)

### `pgbouncer` (extension, recommend_now, 0.80)

Why now:
- High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.

Why not yet:
- Confirm application compatibility with transaction pooling, prepared statements, and session settings.

Next-stage triggers:
- Adopt once pool sizing, failover routing, and idle-session behavior are documented.

Sources:
- `rule-pgbouncer-when-high-concurrency` (0.80)

### `logical_replication_pair` (topology_pattern, recommend_now, 0.78)

Why now:
- A logical replication pair supports validation and controlled cutover for PostgreSQL migrations.

Why not yet:
- DDL drift, sequences, replication lag, and fallback criteria must be owned.

Next-stage triggers:
- Move to blue-green once cutover gates and reverse-plan are written.

Sources:
- `rule-logical-replication-pair-for-blue-green-upgrade` (0.78)

### `brin_append_only_chronological` (index_pattern, recommend_now, 0.76)

Why now:
- BRIN is a low-maintenance fit for large chronological append-only tables.
- Append-heavy chronological data often gets useful pruning from small BRIN indexes.

Why not yet:
- It is weak when data is not physically correlated with time or queries need point lookup.
- BRIN depends on physical correlation and does not replace point-lookup btrees.

Next-stage triggers:
- Add btree companion indexes only for proven tenant, status, or id filters.
- Adopt when time-window scans dominate and table ordering remains correlated.

Sources:
- `rule-partitioning-when-retention-matters` (0.76)
- `rule-brin-for-append-heavy-chronological` (0.70)

### `pgbouncer_in_front` (topology_pattern, recommend_now, 0.76)

Why now:
- Putting PgBouncer in front makes connection admission a topology concern.
- Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.

Why not yet:
- It cannot compensate for long transactions or inefficient queries.
- Pool mode can break session-state assumptions and should be tested with the application.

Next-stage triggers:
- Test failover target changes and pool draining in maintenance runbooks.
- Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

Sources:
- `rule-pgbouncer-when-high-concurrency` (0.76)
- `rule-pgbouncer-in-front-when-many-short-connections` (0.74)

### `no_pooling_high_connections` (anti_pattern_warning, avoid_for_now, 0.76)

Why now:
- High peak connections without pooling evidence risks backend exhaustion and idle-session waste.

Why not yet:
- Application pools may be enough if limits and transaction duration are already disciplined.

Next-stage triggers:
- Add pool sizing, transaction duration, and session-state compatibility checks.

Sources:
- `rule-warn-no-pooling-high-connections` (0.76)

### `blue_green_upgrade_via_logical_replication` (topology_pattern, candidate_later, 0.74)

Why now:
- Blue-green cutover is plausible when logical replication is already part of migration planning.

Why not yet:
- Do not promise near-zero downtime until lag monitoring and reverse-cutover criteria are written.

Next-stage triggers:
- Adopt when dual-write avoidance, validation queries, and rollback owners are agreed.

Sources:
- `rule-logical-replication-for-zero-downtime-migrations` (0.74)

### `btree_composite_equality_then_range` (index_pattern, candidate_later, 0.72)

Why now:
- Hot OLTP and read-heavy filters often need equality columns before range or sort columns.

Why not yet:
- Column order must come from real predicates, not generic indexing instinct.

Next-stage triggers:
- Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

Sources:
- `rule-btree-composite-for-hot-filter-sort` (0.72)

### `primary_with_read_replicas` (topology_pattern, candidate_later, 0.70)

Why now:
- Reporting or read-heavy traffic may need isolation from primary write latency.

Why not yet:
- Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.

Next-stage triggers:
- Adopt when read routing, lag tolerance, and consistency expectations are explicit.

Sources:
- `rule-read-replica-when-reporting-needs-isolation` (0.70)

### `partial_indexes` (core_feature, candidate_later, 0.68)

Why now:
- Large OLTP tables often have small hot subsets that should not force full-table index maintenance.

Why not yet:
- Partial indexes need proven predicates; without query traces they become brittle guesses.

Next-stage triggers:
- Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

Sources:
- `rule-partial-indexes-for-skewed-hot-sets` (0.68)

### `partial_index_for_skew` (index_pattern, candidate_later, 0.68)

Why now:
- The index catalog has a matching pattern for selective predicates on skewed large tables.

Why not yet:
- Wait until the predicate is stable in application SQL and selectivity has been measured.

Next-stage triggers:
- Review index size and write amplification after one representative traffic window.

Sources:
- `rule-partial-indexes-for-skewed-hot-sets` (0.68)

### `materialized_views` (core_feature, candidate_later, 0.67)

Why now:
- Adjacent analytics often needs precomputed read models before replicas or distributed systems.

Why not yet:
- Refresh cadence, staleness tolerance, and locking behavior must be known first.

Next-stage triggers:
- Adopt when repeated aggregate queries dominate total time and stale-enough answers are acceptable.

Sources:
- `rule-materialized-views-for-adjacent-analytics` (0.67)

### `timescaledb` (extension, candidate_later, 0.64)

Why now:
- Very large time-series metrics may benefit from hypertable lifecycle, compression, and retention ergonomics.

Why not yet:
- Core partitioning, BRIN, materialized views, and scheduled retention should be measured first.

Next-stage triggers:
- Revisit when compression, chunk maintenance, and retention automation are measured pain.

Sources:
- `rule-timescaledb-when-centrally-time-series` (0.64)

### `pg_partman` (extension, candidate_later, 0.62)

Why now:
- Recurring time-based partition creation and retention can justify pg_partman automation.

Why not yet:
- The table must already deserve partitioning; pg_partman is not the reason to partition.

Next-stage triggers:
- Adopt when future partition creation or retention jobs become reviewed operational toil.

Sources:
- `rule-pg-partman-when-partitioning-managed-manually` (0.62)

### `pgcrypto` (extension, candidate_later, 0.58)

Why now:
- Database-generated UUID defaults are useful for public identifiers and distributed inserts.

Why not yet:
- Do not treat cryptographic functions as a security architecture without review.

Next-stage triggers:
- Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.

Sources:
- `rule-pgcrypto-for-public-identifiers` (0.58)


## Score Breakdown

- `domain_fit`: 0.72
- `data_shape_fit`: 0.72
- `workload_fit`: 0.79
- `operational_feasibility`: 0.75
- `growth_urgency`: 0.59
- `portability_penalty`: 0.07
- `complexity_penalty`: 0.22

## Warnings

- `no_pooling_high_connections`: High peak connections without pooling evidence risks backend exhaustion and idle-session waste.

## Followup Questions

No followup questions yet.

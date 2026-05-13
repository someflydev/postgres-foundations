# PostgreSQL Architecture Recommendation
Intake: healthcare-telehealth-appointment-platform  |  Generated: 2026-05-13T16:52:14.758852Z
Industry: Healthcare Operations  |  Tenancy: multi_tenant_shared_schema  |  Ops tolerance: medium

## Summary
The intake points to 9 immediate recommendations, 11 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.72
  - Why now: audit_required posture depends on database-enforced state transitions, not only application logging. Relational integrity gives audit reviewers durable evidence that invalid business states were rejected. Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If the audit scope is not yet named, start by identifying which tables and state changes require evidence. If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Add append-only audit tables, actor identity propagation, and retention reviews once regulated workflows are mapped. Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.72 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Row-level Security** — score 0.71
  - Why now: Shared-schema tenancy puts tenant isolation inside every query path. RLS gives the database a backstop when application filters are missed.
  - Why not something else: RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.
  - Triggers for next stage: Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.

- **Declarative Partitioning** — score 0.67
  - Why now: Large append-heavy tables need bounded maintenance, retention, and pruning strategy.
  - Why not something else: Partitioning is premature when tables are modest, retention is vague, or queries do not prune by partition key.
  - Triggers for next stage: Escalate to pg_partman only after manual partition operations become a recurring operational risk.

- **BRIN for Append-only Time** — score 0.67
  - Why now: BRIN is a low-maintenance fit for large chronological append-only tables. Append-heavy chronological data often gets useful pruning from small BRIN indexes.
  - Why not something else: It is weak when data is not physically correlated with time or queries need point lookup. BRIN depends on physical correlation and does not replace point-lookup btrees.
  - Triggers for next stage: Add btree companion indexes only for proven tenant, status, or id filters. Adopt when time-window scans dominate and table ordering remains correlated.

- **PgBouncer** — score 0.67 — [module pgbouncer]
  - Why now: Very high connection peaks are an immediate PostgreSQL operating risk, even before adding larger topology changes. PgBouncer is a narrow, portable operational tool with a clearer runbook than scaling backend process counts indefinitely. High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.
  - Why not something else: Transaction pooling compatibility, prepared statement behavior, and session settings still need an explicit acceptance test. Confirm application compatibility with transaction pooling, prepared statements, and session settings.
  - Triggers for next stage: Adopt with pool sizing, idle timeout, failover routing, and drain procedures documented before the next traffic peak. Adopt once pool sizing, failover routing, and idle-session behavior are documented.

- **Exclusion Constraints** — score 0.66
  - Why now: Scheduling, booking, and availability windows need overlap prevention at write time. Exclusion constraints keep race conditions out of application-only checks.
  - Why not something else: If overlapping rows are allowed by business policy, model the exception first instead of forcing a generic constraint.
  - Triggers for next stage: Escalate to GiST range indexes and concurrency scenarios when double-booking risk is on a hot path.

- **PgBouncer in Front** — score 0.66
  - Why now: At this connection level, pooling belongs in the production topology rather than as an application-side convention. Putting PgBouncer in front makes connection admission a topology concern. Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.
  - Why not something else: Pooler placement must be covered by failover and maintenance runbooks. It cannot compensate for long transactions or inefficient queries. Pool mode can break session-state assumptions and should be tested with the application.
  - Triggers for next stage: Review connection wait time, transaction duration, and pool saturation after one representative traffic window. Test failover target changes and pool draining in maintenance runbooks. Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

- **GiST Range Exclusion** — score 0.65
  - Why now: GiST range indexing supports overlap checks and range predicates for availability data. Range-window workloads need overlap operators and index support.
  - Why not something else: Avoid broad GiST indexes when range predicates are rare or the range column is not selective. Avoid if intervals are rare metadata and not queried or constrained.
  - Triggers for next stage: Add representative concurrent insert tests before relying on the design. Pair with exclusion constraints for correctness-critical scheduling paths.


## Candidate later

- **Composite Equality Then Range** — score 0.64
  - Why now: Hot OLTP and read-heavy filters often need equality columns before range or sort columns.
  - Why not something else: Column order must come from real predicates, not generic indexing instinct.
  - Triggers for next stage: Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

- **Partial Indexes** — score 0.63
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.63
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **Physical Replication** — score 0.59
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.59
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **pg_partman** — score 0.58 — [module pg-partman]
  - Why now: Recurring time-based partition creation and retention can justify pg_partman automation.
  - Why not something else: The table must already deserve partitioning; pg_partman is not the reason to partition.
  - Triggers for next stage: Adopt when future partition creation or retention jobs become reviewed operational toil.

- **Primary With Read Replicas** — score 0.58
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **TimescaleDB** — score 0.56 — [module e5-timescaledb]
  - Why now: Very large time-series metrics may benefit from hypertable lifecycle, compression, and retention ergonomics.
  - Why not something else: Core partitioning, BRIN, materialized views, and scheduled retention should be measured first.
  - Triggers for next stage: Revisit when compression, chunk maintenance, and retention automation are measured pain.

- **pgcrypto** — score 0.55 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.

- **Citus** — score 0.51 — [module e7-citus]
  - Why now: Strong tenant locality and large tables may eventually justify distributed PostgreSQL.
  - Why not something else: Do not adopt Citus until hot reads and writes consistently include a stable distribution key.
  - Triggers for next stage: Revisit after single-primary tuning, partitioning, read replicas, and tenant-local query traces are exhausted.

- **Citus Distributed Cluster** — score 0.48
  - Why now: The topology is plausible only if co-location and cluster operations are explicit.
  - Why not something else: Cluster backup, restore, rebalancing, and query-plan review are substantial operating costs.
  - Triggers for next stage: Adopt only with cluster-aware restore drills and clear shard-key ownership.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **no_pooling_high_connections**: High peak connections without pooling evidence risks backend exhaustion and idle-session waste.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.91 | 0.72 | 0.04 | 0.06 | 0.72 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.90 | 0.81 | 0.04 | 0.12 | 0.72 |
| row_level_security | 0.92 | 0.88 | 0.90 | 0.80 | 0.72 | 0.04 | 0.25 | 0.71 |
| partitioning | 0.76 | 0.86 | 0.84 | 0.76 | 0.88 | 0.04 | 0.30 | 0.67 |
| brin_append_only_chronological | 0.72 | 0.84 | 0.80 | 0.86 | 0.83 | 0.04 | 0.12 | 0.67 |
| pgbouncer | 0.84 | 0.70 | 0.90 | 0.83 | 0.90 | 0.16 | 0.35 | 0.67 |
| exclusion_constraints | 0.78 | 0.90 | 0.72 | 0.83 | 0.70 | 0.04 | 0.17 | 0.66 |
| pgbouncer_in_front | 0.82 | 0.68 | 0.88 | 0.81 | 0.89 | 0.08 | 0.35 | 0.66 |
| gist_range_exclusion | 0.78 | 0.88 | 0.72 | 0.81 | 0.70 | 0.04 | 0.18 | 0.65 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.83 | 0.72 | 0.04 | 0.12 | 0.64 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.79 | 0.77 | 0.04 | 0.16 | 0.63 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.79 | 0.77 | 0.04 | 0.16 | 0.63 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.76 | 0.75 | 0.08 | 0.22 | 0.59 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.78 | 0.70 | 0.04 | 0.18 | 0.59 |
| pg_partman | 0.64 | 0.82 | 0.74 | 0.64 | 0.85 | 0.20 | 0.38 | 0.58 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.70 | 0.75 | 0.10 | 0.35 | 0.58 |
| timescaledb | 0.68 | 0.86 | 0.76 | 0.47 | 0.88 | 0.22 | 0.72 | 0.56 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.86 | 0.59 | 0.04 | 0.12 | 0.55 |
| citus | 0.66 | 0.70 | 0.76 | 0.41 | 0.87 | 0.28 | 0.72 | 0.51 |
| citus_distributed_cluster | 0.64 | 0.68 | 0.72 | 0.38 | 0.86 | 0.30 | 0.72 | 0.48 |


## Cited rules
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-rls-when-multi-tenant-and-shared-schema (contrib 0.88)
- rule-partitioning-when-retention-matters (contrib 0.80)
- rule-brin-for-append-heavy-chronological (contrib 0.70)
- rule-pgbouncer-now-for-very-high-concurrency (contrib 0.90)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-exclusion-constraints-for-overlap-windows (contrib 0.82)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-gist-for-range-overlap (contrib 0.76)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pg-partman-when-partitioning-managed-manually (contrib 0.62)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-timescaledb-when-centrally-time-series (contrib 0.64)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-citus-only-with-distribution-key (contrib 0.60)
- rule-warn-no-pooling-high-connections (contrib 0.76)


## Next steps (90-day horizon)
1. Convert each recommend-now item into a small implementation or validation plan with owner, rollback criteria, and acceptance checks.
2. Capture the workload evidence needed to promote or reject candidate-later items.
3. Resolve avoid-for-now warnings before adding topology, extension, or indexing complexity.

## Notes and caveats
- Scores are decision support, not an automatic architecture approval.
- Penalty dimensions are shown as positive values in the table and subtracted by the weighted model.


## Appendix: full intake
<details>
<summary>Full intake JSON</summary>

```json
{
  "as_of_date": "2026-05-12",
  "data_shapes": [
    "relational_core",
    "ranges_windows",
    "append_only_events",
    "time_series_metrics"
  ],
  "existing_postgres_topology": "primary_with_read_replicas",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "They need tenant isolation, exclusion-style booking protection, and a posture on whether time-series tooling is justified for video-quality metrics. Provider groups behave like tenants, but patients move between groups after insurance changes, so isolation cannot erase cross-group care workflows. Growth horizon: 6, 12, and 24 months. Restore drills are not documented.",
  "intake_id": "healthcare-telehealth-appointment-platform",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "healthcare_ops",
    "managed_service_requirement": "strongly_preferred",
    "operational_tolerance": "medium",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 64
  },
  "scale_signals": {
    "concurrent_connections_peak": 2100,
    "growth_rate_month_over_month": 0.17,
    "read_throughput_qps": 7800,
    "row_counts_largest_tables": {
      "appointments": 88000000,
      "availability_windows": 260000000,
      "video_session_events": 340000000
    },
    "write_throughput_rows_per_sec": 1700
  },
  "security_constraints": [
    "hipaa",
    "pii_in_scope",
    "audit_required",
    "rls_required"
  ],
  "tenancy_model": "multi_tenant_shared_schema",
  "workload_patterns": [
    "oltp_heavy",
    "append_heavy",
    "read_heavy",
    "strong_tenant_locality"
  ]
}
```

</details>
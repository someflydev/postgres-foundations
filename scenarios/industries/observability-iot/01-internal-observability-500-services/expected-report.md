# PostgreSQL Architecture Recommendation
Intake: observability-internal-500-services  |  Generated: 2026-05-13T16:52:16.145473Z
Industry: Observability and IoT  |  Tenancy: single_tenant  |  Ops tolerance: medium

## Summary
The intake points to 4 immediate recommendations, 11 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. No anti-pattern warning matched this intake.

## Recommend now

- **Constraints** — score 0.71
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.71 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Declarative Partitioning** — score 0.67
  - Why now: Large append-heavy tables need bounded maintenance, retention, and pruning strategy.
  - Why not something else: Partitioning is premature when tables are modest, retention is vague, or queries do not prune by partition key.
  - Triggers for next stage: Escalate to pg_partman only after manual partition operations become a recurring operational risk.

- **BRIN for Append-only Time** — score 0.67
  - Why now: BRIN is a low-maintenance fit for large chronological append-only tables. Append-heavy chronological data often gets useful pruning from small BRIN indexes.
  - Why not something else: It is weak when data is not physically correlated with time or queries need point lookup. BRIN depends on physical correlation and does not replace point-lookup btrees.
  - Triggers for next stage: Add btree companion indexes only for proven tenant, status, or id filters. Adopt when time-window scans dominate and table ordering remains correlated.


## Candidate later

- **Composite Equality Then Range** — score 0.63
  - Why now: Hot OLTP and read-heavy filters often need equality columns before range or sort columns.
  - Why not something else: Column order must come from real predicates, not generic indexing instinct.
  - Triggers for next stage: Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

- **Partial Indexes** — score 0.62
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.62
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **Materialized Views** — score 0.59
  - Why now: Adjacent analytics often needs precomputed read models before replicas or distributed systems.
  - Why not something else: Refresh cadence, staleness tolerance, and locking behavior must be known first.
  - Triggers for next stage: Adopt when repeated aggregate queries dominate total time and stale-enough answers are acceptable.

- **Physical Replication** — score 0.58
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.58
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **PgBouncer** — score 0.58 — [module pgbouncer]
  - Why now: High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.
  - Why not something else: Confirm application compatibility with transaction pooling, prepared statements, and session settings. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Adopt once pool sizing, failover routing, and idle-session behavior are documented.

- **PgBouncer in Front** — score 0.58
  - Why now: Putting PgBouncer in front makes connection admission a topology concern. Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.
  - Why not something else: It cannot compensate for long transactions or inefficient queries. Pool mode can break session-state assumptions and should be tested with the application. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Test failover target changes and pool draining in maintenance runbooks. Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

- **Primary With Read Replicas** — score 0.57
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **pg_partman** — score 0.57 — [module pg-partman]
  - Why now: Recurring time-based partition creation and retention can justify pg_partman automation.
  - Why not something else: The table must already deserve partitioning; pg_partman is not the reason to partition.
  - Triggers for next stage: Adopt when future partition creation or retention jobs become reviewed operational toil.

- **TimescaleDB** — score 0.55 — [module e5-timescaledb]
  - Why now: Very large time-series metrics may benefit from hypertable lifecycle, compression, and retention ergonomics.
  - Why not something else: Core partitioning, BRIN, materialized views, and scheduled retention should be measured first.
  - Triggers for next stage: Revisit when compression, chunk maintenance, and retention automation are measured pain.


## Not enough evidence

- **pgvector** — score 0.37 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- No anti-pattern warnings matched.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.86 | 0.72 | 0.04 | 0.06 | 0.71 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.85 | 0.81 | 0.04 | 0.12 | 0.71 |
| partitioning | 0.76 | 0.86 | 0.84 | 0.71 | 0.88 | 0.04 | 0.30 | 0.67 |
| brin_append_only_chronological | 0.72 | 0.84 | 0.80 | 0.81 | 0.83 | 0.04 | 0.12 | 0.67 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.79 | 0.72 | 0.04 | 0.12 | 0.63 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.74 | 0.77 | 0.04 | 0.16 | 0.62 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.74 | 0.77 | 0.04 | 0.16 | 0.62 |
| materialized_views | 0.66 | 0.66 | 0.74 | 0.77 | 0.71 | 0.04 | 0.16 | 0.59 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.71 | 0.75 | 0.08 | 0.22 | 0.58 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.73 | 0.70 | 0.04 | 0.18 | 0.58 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.68 | 0.78 | 0.24 | 0.35 | 0.58 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.65 | 0.78 | 0.12 | 0.35 | 0.58 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.65 | 0.75 | 0.10 | 0.35 | 0.57 |
| pg_partman | 0.64 | 0.82 | 0.74 | 0.59 | 0.85 | 0.24 | 0.38 | 0.57 |
| timescaledb | 0.68 | 0.86 | 0.76 | 0.42 | 0.88 | 0.24 | 0.72 | 0.55 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.55 | 0.59 | 0.08 | 0.72 | 0.37 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-partitioning-when-retention-matters (contrib 0.80)
- rule-brin-for-append-heavy-chronological (contrib 0.70)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-materialized-views-for-adjacent-analytics (contrib 0.67)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-pg-partman-when-partitioning-managed-manually (contrib 0.62)
- rule-timescaledb-when-centrally-time-series (contrib 0.64)
- rule-pgvector-not-yet-without-embeddings (contrib 0.56)


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
    "append_only_events",
    "time_series_metrics"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "timescaledb",
      "reason": "The platform team wants to know whether hypertables are justified."
    }
  ],
  "free_form_notes": "The team needs retention by service and day, BRIN-friendly time-window scans, and materialized rollups for dashboards. TimescaleDB is plausible later, but the first pain is disciplined core partitioning and owned retention jobs.",
  "intake_id": "observability-internal-500-services",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "observability_iot",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "medium",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 12
  },
  "scale_signals": {
    "concurrent_connections_peak": 260,
    "growth_rate_month_over_month": 0.09,
    "read_throughput_qps": 1300,
    "row_counts_largest_tables": {
      "log_events": 78000000,
      "metric_samples": 135000000,
      "service_catalog": 1200
    },
    "write_throughput_rows_per_sec": 950
  },
  "security_constraints": [],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "append_heavy",
    "analytics_adjacent",
    "read_heavy"
  ]
}
```

</details>
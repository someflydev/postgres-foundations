# PostgreSQL Architecture Recommendation
Intake: logistics-global-fleet-analytics  |  Generated: 2026-05-13T16:52:15.605360Z
Industry: Logistics and Geospatial Operations  |  Tenancy: single_tenant  |  Ops tolerance: high

## Summary
The intake points to 7 immediate recommendations, 10 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.72
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.72 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **PostGIS** — score 0.72 — [module e3-postgis]
  - Why now: Geo-query-heavy workloads need spatial types, predicates, and indexes rather than latitude/longitude conventions. PostGIS keeps spatial decisions close to transactional state.
  - Why not something else: PostGIS is not needed for display-only coordinates or rare exports with no spatial predicates.
  - Triggers for next stage: Add geometry validity, coordinate-system rules, and restore validation before production rollout.

- **GiST Geospatial** — score 0.70
  - Why now: GiST spatial indexes are the expected access path for containment, intersection, and distance predicates.
  - Why not something else: Index choice should wait if the product only stores points for display.
  - Triggers for next stage: Benchmark representative bounding-box and nearest-neighbor queries.

- **Declarative Partitioning** — score 0.68
  - Why now: Large append-heavy tables need bounded maintenance, retention, and pruning strategy.
  - Why not something else: Partitioning is premature when tables are modest, retention is vague, or queries do not prune by partition key.
  - Triggers for next stage: Escalate to pg_partman only after manual partition operations become a recurring operational risk.

- **BRIN for Append-only Time** — score 0.68
  - Why now: BRIN is a low-maintenance fit for large chronological append-only tables. Append-heavy chronological data often gets useful pruning from small BRIN indexes.
  - Why not something else: It is weak when data is not physically correlated with time or queries need point lookup. BRIN depends on physical correlation and does not replace point-lookup btrees.
  - Triggers for next stage: Add btree companion indexes only for proven tenant, status, or id filters. Adopt when time-window scans dominate and table ordering remains correlated.

- **TimescaleDB** — score 0.67 — [module e5-timescaledb]
  - Why now: Large central time-series tables plus adjacent analytics create recurring chunk, retention, compression, and aggregate-maintenance work. At this scale, TimescaleDB is justified only because the workload has crossed beyond one-off partition maintenance. Very large time-series metrics may benefit from hypertable lifecycle, compression, and retention ergonomics.
  - Why not something else: Do not adopt if the managed-service target cannot support extension upgrades, restore drills, and retention runbooks. Core partitioning, BRIN, materialized views, and scheduled retention should be measured first.
  - Triggers for next stage: Adopt with documented compression policy, continuous aggregate ownership, restore testing, and rollback criteria. Revisit when compression, chunk maintenance, and retention automation are measured pain.


## Candidate later

- **Composite Equality Then Range** — score 0.65
  - Why now: Hot OLTP and read-heavy filters often need equality columns before range or sort columns.
  - Why not something else: Column order must come from real predicates, not generic indexing instinct.
  - Triggers for next stage: Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

- **Partial Indexes** — score 0.64
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.64
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **Materialized Views** — score 0.60
  - Why now: Adjacent analytics often needs precomputed read models before replicas or distributed systems.
  - Why not something else: Refresh cadence, staleness tolerance, and locking behavior must be known first.
  - Triggers for next stage: Adopt when repeated aggregate queries dominate total time and stale-enough answers are acceptable.

- **PgBouncer** — score 0.60 — [module pgbouncer]
  - Why now: High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.
  - Why not something else: Confirm application compatibility with transaction pooling, prepared statements, and session settings. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Adopt once pool sizing, failover routing, and idle-session behavior are documented.

- **Physical Replication** — score 0.59
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.59
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **PgBouncer in Front** — score 0.59
  - Why now: Putting PgBouncer in front makes connection admission a topology concern. Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.
  - Why not something else: It cannot compensate for long transactions or inefficient queries. Pool mode can break session-state assumptions and should be tested with the application. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Test failover target changes and pool draining in maintenance runbooks. Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

- **pg_partman** — score 0.59 — [module pg-partman]
  - Why now: Recurring time-based partition creation and retention can justify pg_partman automation.
  - Why not something else: The table must already deserve partitioning; pg_partman is not the reason to partition.
  - Triggers for next stage: Adopt when future partition creation or retention jobs become reviewed operational toil.

- **Primary With Read Replicas** — score 0.59
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **no_pooling_high_connections**: High peak connections without pooling evidence risks backend exhaustion and idle-session waste.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.95 | 0.72 | 0.04 | 0.06 | 0.72 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.94 | 0.81 | 0.04 | 0.12 | 0.72 |
| postgis | 0.90 | 0.94 | 0.90 | 0.79 | 0.75 | 0.08 | 0.35 | 0.72 |
| gist_geospatial | 0.86 | 0.90 | 0.86 | 0.83 | 0.72 | 0.06 | 0.22 | 0.70 |
| partitioning | 0.76 | 0.86 | 0.84 | 0.79 | 0.88 | 0.04 | 0.30 | 0.68 |
| brin_append_only_chronological | 0.72 | 0.84 | 0.80 | 0.90 | 0.83 | 0.04 | 0.12 | 0.68 |
| timescaledb | 0.82 | 0.92 | 0.88 | 0.69 | 0.94 | 0.20 | 0.72 | 0.67 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.87 | 0.72 | 0.04 | 0.12 | 0.65 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.82 | 0.77 | 0.04 | 0.16 | 0.64 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.82 | 0.77 | 0.04 | 0.16 | 0.64 |
| materialized_views | 0.66 | 0.66 | 0.74 | 0.86 | 0.71 | 0.04 | 0.16 | 0.60 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.76 | 0.78 | 0.16 | 0.35 | 0.60 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.79 | 0.75 | 0.08 | 0.22 | 0.59 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.82 | 0.70 | 0.04 | 0.18 | 0.59 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.74 | 0.78 | 0.12 | 0.35 | 0.59 |
| pg_partman | 0.64 | 0.82 | 0.74 | 0.67 | 0.85 | 0.20 | 0.38 | 0.59 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.74 | 0.75 | 0.10 | 0.35 | 0.59 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-postgis-for-geo-query-heavy (contrib 0.88)
- rule-partitioning-when-retention-matters (contrib 0.80)
- rule-brin-for-append-heavy-chronological (contrib 0.70)
- rule-timescaledb-now-for-mature-time-series (contrib 0.84)
- rule-timescaledb-when-centrally-time-series (contrib 0.64)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-materialized-views-for-adjacent-analytics (contrib 0.67)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-pg-partman-when-partitioning-managed-manually (contrib 0.62)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
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
    "geospatial",
    "append_only_events",
    "time_series_metrics"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "postgis",
      "reason": "Spatial joins and distance buckets are central to analytics."
    },
    {
      "extension_slug": "timescaledb",
      "reason": "Retention, compression, and continuous rollups are measured operational pain."
    }
  ],
  "free_form_notes": "The fleet analytics group runs regional heat maps, corridor dwell-time analysis, and spatial compliance reporting. Data is centrally time-keyed and old partitions are expensive to manage. They need not shard yet because queries are regional/time bounded, not tenant-local.",
  "intake_id": "logistics-global-fleet-analytics",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "logistics_geo",
    "managed_service_requirement": "strongly_preferred",
    "operational_tolerance": "high",
    "portability_constraints": [
      "aws_rds",
      "azure_pg"
    ],
    "team_size_engineers": 28
  },
  "scale_signals": {
    "concurrent_connections_peak": 850,
    "growth_rate_month_over_month": 0.16,
    "read_throughput_qps": 4200,
    "row_counts_largest_tables": {
      "facilities": 65000,
      "fleet_positions": 880000000,
      "route_events": 540000000
    },
    "write_throughput_rows_per_sec": 2100
  },
  "security_constraints": [
    "pii_in_scope",
    "gdpr_dsr"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "read_heavy",
    "append_heavy",
    "analytics_adjacent",
    "geo_query_heavy"
  ]
}
```

</details>
# PostgreSQL Architecture Recommendation
Intake: logistics-geo-minimal  |  Generated: 2026-05-13T16:25:57.709570Z
Industry: Logistics and Geospatial Operations  |  Tenancy: multi_tenant_shared_schema  |  Ops tolerance: medium

## Summary
The intake points to 6 immediate recommendations, 8 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.71
  - Why now: audit_required posture depends on database-enforced state transitions, not only application logging. Relational integrity gives audit reviewers durable evidence that invalid business states were rejected. Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If the audit scope is not yet named, start by identifying which tables and state changes require evidence. If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Add append-only audit tables, actor identity propagation, and retention reviews once regulated workflows are mapped. Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.71 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **PostGIS** — score 0.70 — [module e3-postgis]
  - Why now: Geo-query-heavy workloads need spatial types, predicates, and indexes rather than latitude/longitude conventions. PostGIS keeps spatial decisions close to transactional state.
  - Why not something else: PostGIS is not needed for display-only coordinates or rare exports with no spatial predicates.
  - Triggers for next stage: Add geometry validity, coordinate-system rules, and restore validation before production rollout.

- **GiST Geospatial** — score 0.69
  - Why now: GiST spatial indexes are the expected access path for containment, intersection, and distance predicates.
  - Why not something else: Index choice should wait if the product only stores points for display.
  - Triggers for next stage: Benchmark representative bounding-box and nearest-neighbor queries.

- **Row-level Security** — score 0.67
  - Why now: Shared-schema tenancy puts tenant isolation inside every query path. RLS gives the database a backstop when application filters are missed.
  - Why not something else: RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.
  - Triggers for next stage: Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.

- **Exclusion Constraints** — score 0.66
  - Why now: Scheduling, booking, and availability windows need overlap prevention at write time. Exclusion constraints keep race conditions out of application-only checks.
  - Why not something else: If overlapping rows are allowed by business policy, model the exception first instead of forcing a generic constraint.
  - Triggers for next stage: Escalate to GiST range indexes and concurrency scenarios when double-booking risk is on a hot path.


## Candidate later

- **GiST Range Exclusion** — score 0.65
  - Why now: GiST range indexing supports overlap checks and range predicates for availability data. Range-window workloads need overlap operators and index support.
  - Why not something else: Avoid broad GiST indexes when range predicates are rare or the range column is not selective. Avoid if intervals are rare metadata and not queried or constrained. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Add representative concurrent insert tests before relying on the design. Pair with exclusion constraints for correctness-critical scheduling paths.

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

- **Physical Replication** — score 0.58
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.58
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **Primary With Read Replicas** — score 0.57
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **pgcrypto** — score 0.54 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- **pgvector** — score 0.37 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- **geo_logic_without_postgis**: Geo-heavy logic without PostGIS evidence risks incorrect distance, containment, and indexing behavior.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.86 | 0.72 | 0.04 | 0.06 | 0.71 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.85 | 0.81 | 0.04 | 0.12 | 0.71 |
| postgis | 0.90 | 0.94 | 0.90 | 0.70 | 0.75 | 0.08 | 0.35 | 0.70 |
| gist_geospatial | 0.86 | 0.90 | 0.86 | 0.75 | 0.72 | 0.06 | 0.22 | 0.69 |
| row_level_security | 0.86 | 0.82 | 0.84 | 0.75 | 0.72 | 0.04 | 0.25 | 0.67 |
| exclusion_constraints | 0.78 | 0.90 | 0.72 | 0.79 | 0.70 | 0.04 | 0.17 | 0.66 |
| gist_range_exclusion | 0.78 | 0.88 | 0.72 | 0.76 | 0.70 | 0.04 | 0.18 | 0.65 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.79 | 0.72 | 0.04 | 0.12 | 0.63 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.74 | 0.77 | 0.04 | 0.16 | 0.62 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.74 | 0.77 | 0.04 | 0.16 | 0.62 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.71 | 0.75 | 0.08 | 0.22 | 0.58 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.73 | 0.70 | 0.04 | 0.18 | 0.58 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.65 | 0.75 | 0.10 | 0.35 | 0.57 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.81 | 0.59 | 0.04 | 0.12 | 0.54 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.55 | 0.59 | 0.08 | 0.72 | 0.37 |


## Cited rules
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-postgis-for-geo-query-heavy (contrib 0.88)
- rule-rls-when-multi-tenant-and-shared-schema (contrib 0.88)
- rule-exclusion-constraints-for-overlap-windows (contrib 0.82)
- rule-gist-for-range-overlap (contrib 0.76)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-pgvector-not-yet-without-embeddings (contrib 0.56)
- rule-warn-geo-logic-without-postgis (contrib 0.82)


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
    "ranges_windows"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "Dispatch and service-zone queries need distance, containment, and nearest facility logic. Product is not asking for semantic search.",
  "intake_id": "logistics-geo-minimal",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "logistics_geo",
    "managed_service_requirement": "strongly_preferred",
    "operational_tolerance": "medium",
    "portability_constraints": [
      "any_managed"
    ],
    "team_size_engineers": 12
  },
  "scale_signals": {
    "concurrent_connections_peak": 180,
    "growth_rate_month_over_month": 0.09,
    "largest_object_bytes": 524288,
    "read_throughput_qps": 1800,
    "row_counts_largest_tables": {
      "shipments": 18000000,
      "tracking_events": 72000000
    },
    "write_throughput_rows_per_sec": 220
  },
  "security_constraints": [
    "audit_required",
    "pii_in_scope"
  ],
  "tenancy_model": "multi_tenant_shared_schema",
  "workload_patterns": [
    "oltp_heavy",
    "geo_query_heavy",
    "read_heavy"
  ]
}
```

</details>
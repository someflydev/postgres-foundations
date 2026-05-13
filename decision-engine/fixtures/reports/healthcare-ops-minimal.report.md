# PostgreSQL Architecture Recommendation
Intake: healthcare-ops-minimal  |  Generated: 2026-05-13T16:25:57.296235Z
Industry: Healthcare Operations  |  Tenancy: multi_tenant_database_per_tenant  |  Ops tolerance: low

## Summary
The intake points to 2 immediate recommendations, 11 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.69
  - Why now: audit_required posture depends on database-enforced state transitions, not only application logging. Relational integrity gives audit reviewers durable evidence that invalid business states were rejected. Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If the audit scope is not yet named, start by identifying which tables and state changes require evidence. If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Add append-only audit tables, actor identity propagation, and retention reviews once regulated workflows are mapped. Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.69 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.


## Candidate later

- **Exclusion Constraints** — score 0.63
  - Why now: Scheduling, booking, and availability windows need overlap prevention at write time. Exclusion constraints keep race conditions out of application-only checks.
  - Why not something else: If overlapping rows are allowed by business policy, model the exception first instead of forcing a generic constraint. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Escalate to GiST range indexes and concurrency scenarios when double-booking risk is on a hot path.

- **GiST Range Exclusion** — score 0.62
  - Why now: GiST range indexing supports overlap checks and range predicates for availability data. Range-window workloads need overlap operators and index support.
  - Why not something else: Avoid broad GiST indexes when range predicates are rare or the range column is not selective. Avoid if intervals are rare metadata and not queried or constrained. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Add representative concurrent insert tests before relying on the design. Pair with exclusion constraints for correctness-critical scheduling paths.

- **Composite Equality Then Range** — score 0.61
  - Why now: Hot OLTP and read-heavy filters often need equality columns before range or sort columns.
  - Why not something else: Column order must come from real predicates, not generic indexing instinct.
  - Triggers for next stage: Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

- **Partial Indexes** — score 0.60
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.60
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **postgres_fdw** — score 0.59 — [module e6-postgres-fdw]
  - Why now: The intake names remote PostgreSQL access and an FDW federation need. postgres_fdw is the narrowest PostgreSQL-native bridge when remote paths are bounded.
  - Why not something else: FDW should not become a hidden permanent hot path without pushdown verification and retirement planning. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Require EXPLAIN VERBOSE pushdown checks and a materialization plan for hot remote reads.

- **postgres_fdw Federation** — score 0.57
  - Why now: A federation topology makes ownership and remote failure modes explicit. Migration-bridge workloads need explicit remote-source boundaries and owner-visible failure modes.
  - Why not something else: Avoid broad cross-database joins until latency and remote-owner behavior are understood. Avoid broad permanent federation without pushdown checks and decommission criteria. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Document credentials, remote health monitoring, and fallback behavior. Adopt once remote credentials, latency SLOs, and fallback behavior are documented.

- **Physical Replication** — score 0.56
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.55
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **Primary With Read Replicas** — score 0.55
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **pgcrypto** — score 0.51 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **no_restore_drills**: Low operational tolerance plus complex data or bridge needs requires restore proof before adopting more moving parts.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.55 | 0.04 | 0.06 | 0.69 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.81 | 0.63 | 0.04 | 0.12 | 0.69 |
| exclusion_constraints | 0.78 | 0.90 | 0.72 | 0.74 | 0.52 | 0.04 | 0.17 | 0.63 |
| gist_range_exclusion | 0.78 | 0.88 | 0.72 | 0.72 | 0.52 | 0.04 | 0.18 | 0.62 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.74 | 0.55 | 0.04 | 0.12 | 0.61 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.70 | 0.59 | 0.04 | 0.16 | 0.60 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.70 | 0.59 | 0.04 | 0.16 | 0.60 |
| postgres_fdw | 0.78 | 0.80 | 0.78 | 0.61 | 0.55 | 0.08 | 0.35 | 0.59 |
| postgres_fdw_federation | 0.78 | 0.76 | 0.74 | 0.58 | 0.53 | 0.10 | 0.35 | 0.57 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.67 | 0.57 | 0.08 | 0.22 | 0.56 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.69 | 0.52 | 0.04 | 0.18 | 0.55 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.61 | 0.57 | 0.10 | 0.35 | 0.55 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.77 | 0.41 | 0.04 | 0.12 | 0.51 |


## Cited rules
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-exclusion-constraints-for-overlap-windows (contrib 0.82)
- rule-gist-for-range-overlap (contrib 0.76)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-postgres-fdw-for-federation (contrib 0.80)
- rule-fdw-federation-for-modernization-bridge (contrib 0.74)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-warn-no-restore-drills (contrib 0.68)


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
    "foreign_postgres_access"
  ],
  "existing_postgres_topology": "primary_with_read_replicas",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "postgres_fdw",
      "reason": "Short-lived read-only access is needed for legacy scheduling data during cutover."
    }
  ],
  "free_form_notes": "Healthcare operations system with legacy bridge needs and low operational tolerance.",
  "intake_id": "healthcare-ops-minimal",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": true,
    "has_legacy_postgres_source": true,
    "requires_federation_via_fdw": true,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "healthcare_ops",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "gcp_cloud_sql",
      "any_managed"
    ],
    "team_size_engineers": 9
  },
  "scale_signals": {
    "concurrent_connections_peak": 160,
    "growth_rate_month_over_month": 0.07,
    "read_throughput_qps": 1100,
    "row_counts_largest_tables": {
      "appointments": 9000000,
      "audit_log": 60000000
    },
    "write_throughput_rows_per_sec": 95
  },
  "security_constraints": [
    "audit_required",
    "pii_in_scope",
    "hipaa"
  ],
  "tenancy_model": "multi_tenant_database_per_tenant",
  "workload_patterns": [
    "oltp_heavy",
    "read_heavy",
    "migration_bridge"
  ]
}
```

</details>
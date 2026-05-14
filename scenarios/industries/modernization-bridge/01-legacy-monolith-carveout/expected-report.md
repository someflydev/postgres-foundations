# PostgreSQL Architecture Recommendation
Intake: modernization-legacy-monolith-carveout  |  Generated: 2026-05-14T07:31:50.140671Z
Industry: Modernization Bridge  |  Tenancy: single_tenant  |  Ops tolerance: low

## Summary
The intake points to 3 immediate recommendations, 10 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 2 anti-patterns that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.70
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.70 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **postgres_fdw** — score 0.68 — [module e6-postgres-fdw]
  - Why now: The intake names remote PostgreSQL access and an FDW federation need. postgres_fdw is the narrowest PostgreSQL-native bridge when remote paths are bounded.
  - Why not something else: FDW should not become a hidden permanent hot path without pushdown verification and retirement planning.
  - Triggers for next stage: Require EXPLAIN VERBOSE pushdown checks and a materialization plan for hot remote reads.


## Candidate later

- **Composite Equality Then Range** — score 0.62
  - Why now: Hot OLTP and read-heavy filters often need equality columns before range or sort columns.
  - Why not something else: Column order must come from real predicates, not generic indexing instinct.
  - Triggers for next stage: Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

- **Partial Indexes** — score 0.61
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.61
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **postgres_fdw Federation** — score 0.58
  - Why now: A federation topology makes ownership and remote failure modes explicit. Migration-bridge workloads need explicit remote-source boundaries and owner-visible failure modes.
  - Why not something else: Avoid broad cross-database joins until latency and remote-owner behavior are understood. Avoid broad permanent federation without pushdown checks and decommission criteria. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Document credentials, remote health monitoring, and fallback behavior. Adopt once remote credentials, latency SLOs, and fallback behavior are documented.

- **Physical Replication** — score 0.57
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **PgBouncer** — score 0.56 — [module pgbouncer]
  - Why now: High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.
  - Why not something else: Confirm application compatibility with transaction pooling, prepared statements, and session settings. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Adopt once pool sizing, failover routing, and idle-session behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.56
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **PgBouncer in Front** — score 0.56
  - Why now: Putting PgBouncer in front makes connection admission a topology concern. Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.
  - Why not something else: It cannot compensate for long transactions or inefficient queries. Pool mode can break session-state assumptions and should be tested with the application. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Test failover target changes and pool draining in maintenance runbooks. Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

- **Primary With Read Replicas** — score 0.56
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **pgcrypto** — score 0.52 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **shard_without_distribution_key**: Citus is being considered, but the intake also names managed-service portability as a hard constraint.; Treat distributed PostgreSQL as blocked until portability, restore, and distribution-key evidence are resolved.; Citus bias without strong tenant locality suggests distribution before a distribution key is proven.

- **no_restore_drills**: Low operational tolerance plus complex data or bridge needs requires restore proof before adopting more moving parts.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.64 | 0.04 | 0.06 | 0.70 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.81 | 0.72 | 0.04 | 0.12 | 0.70 |
| postgres_fdw | 0.88 | 0.90 | 0.88 | 0.71 | 0.70 | 0.08 | 0.35 | 0.68 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.74 | 0.64 | 0.04 | 0.12 | 0.62 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.70 | 0.68 | 0.04 | 0.16 | 0.61 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.70 | 0.68 | 0.04 | 0.16 | 0.61 |
| postgres_fdw_federation | 0.78 | 0.76 | 0.74 | 0.58 | 0.62 | 0.10 | 0.35 | 0.58 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.67 | 0.66 | 0.08 | 0.22 | 0.57 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.64 | 0.69 | 0.24 | 0.35 | 0.56 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.69 | 0.61 | 0.04 | 0.18 | 0.56 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.61 | 0.69 | 0.12 | 0.35 | 0.56 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.61 | 0.66 | 0.10 | 0.35 | 0.56 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.77 | 0.50 | 0.04 | 0.12 | 0.52 |
| citus | 0.48 | 0.58 | 0.42 | 0.28 | 0.65 | 0.36 | 0.72 | 0.33 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-postgres-fdw-for-federation (contrib 0.80)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-fdw-federation-for-modernization-bridge (contrib 0.74)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-warn-citus-portability-rejection (contrib 0.84)
- rule-warn-shard-without-distribution-key (contrib 0.80)
- rule-warn-no-restore-drills (contrib 0.68)
- rule-citus-avoid-without-portable-distribution-key (contrib 0.82)


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
    "foreign_postgres_access"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [
    {
      "extension_slug": "citus",
      "reason": "AWS RDS portability and no distribution key make Citus inappropriate now."
    }
  ],
  "explicit_bias_for": [
    {
      "extension_slug": "postgres_fdw",
      "reason": "Carveout needs bounded validation reads from the old PostgreSQL monolith."
    },
    {
      "extension_slug": "citus",
      "reason": "An executive asked whether the new platform should start distributed."
    }
  ],
  "free_form_notes": "The new service must read a narrow customer and order slice from the old PostgreSQL monolith during carveout. Logical replication may become useful for cutover later, but initial need is FDW with pushdown checks and a retirement plan. Citus is blocked by portability and absent distribution-key evidence.",
  "intake_id": "modernization-legacy-monolith-carveout",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": true,
    "requires_federation_via_fdw": true,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "modernization_bridge",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 11
  },
  "scale_signals": {
    "concurrent_connections_peak": 260,
    "growth_rate_month_over_month": 0.04,
    "read_throughput_qps": 1100,
    "row_counts_largest_tables": {
      "audit_events": 94000000,
      "customer_profiles": 8500000,
      "orders": 42000000
    },
    "write_throughput_rows_per_sec": 220
  },
  "security_constraints": [
    "pii_in_scope"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "oltp_heavy",
    "migration_bridge",
    "read_heavy"
  ]
}
```

</details>

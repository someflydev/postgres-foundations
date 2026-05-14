# PostgreSQL Architecture Recommendation
Intake: modernization-multi-database-consolidation  |  Generated: 2026-05-14T07:31:50.456680Z
Industry: Modernization Bridge  |  Tenancy: single_tenant  |  Ops tolerance: medium

## Summary
The intake points to 5 immediate recommendations, 11 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Logical Replication** — score 0.72
  - Why now: A PostgreSQL source plus zero-downtime migration need is a direct fit for publication/subscription cutover.
  - Why not something else: Logical replication still needs primary keys, DDL choreography, sequence handling, and rollback planning.
  - Triggers for next stage: Move to a blue-green topology once replication lag, cutover checks, and write-freeze windows are defined.

- **Constraints** — score 0.70
  - Why now: audit_required posture depends on database-enforced state transitions, not only application logging. Relational integrity gives audit reviewers durable evidence that invalid business states were rejected. Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If the audit scope is not yet named, start by identifying which tables and state changes require evidence. If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Add append-only audit tables, actor identity propagation, and retention reviews once regulated workflows are mapped. Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.70 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Logical Replication Pair** — score 0.70
  - Why now: A logical replication pair supports validation and controlled cutover for PostgreSQL migrations.
  - Why not something else: DDL drift, sequences, replication lag, and fallback criteria must be owned.
  - Triggers for next stage: Move to blue-green once cutover gates and reverse-plan are written.

- **postgres_fdw** — score 0.69 — [module e6-postgres-fdw]
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

- **PgBouncer** — score 0.58 — [module pgbouncer]
  - Why now: High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.
  - Why not something else: Confirm application compatibility with transaction pooling, prepared statements, and session settings. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Adopt once pool sizing, failover routing, and idle-session behavior are documented.

- **Physical Replication** — score 0.57
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.57
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **PgBouncer in Front** — score 0.57
  - Why now: Putting PgBouncer in front makes connection admission a topology concern. Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.
  - Why not something else: It cannot compensate for long transactions or inefficient queries. Pool mode can break session-state assumptions and should be tested with the application. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Test failover target changes and pool draining in maintenance runbooks. Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

- **Primary With Read Replicas** — score 0.56
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **Blue-green Upgrade via Logical Replication** — score 0.56
  - Why now: Blue-green cutover is plausible when logical replication is already part of migration planning.
  - Why not something else: Do not promise near-zero downtime until lag monitoring and reverse-cutover criteria are written.
  - Triggers for next stage: Adopt when dual-write avoidance, validation queries, and rollback owners are agreed.

- **pgcrypto** — score 0.53 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **no_pooling_high_connections**: High peak connections without pooling evidence risks backend exhaustion and idle-session waste.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| logical_replication | 0.90 | 0.82 | 0.94 | 0.82 | 0.82 | 0.08 | 0.20 | 0.72 |
| constraints | 0.86 | 0.90 | 0.82 | 0.86 | 0.64 | 0.04 | 0.06 | 0.70 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.85 | 0.72 | 0.04 | 0.12 | 0.70 |
| logical_replication_pair | 0.90 | 0.82 | 0.94 | 0.77 | 0.81 | 0.10 | 0.35 | 0.70 |
| postgres_fdw | 0.88 | 0.90 | 0.88 | 0.76 | 0.70 | 0.08 | 0.35 | 0.69 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.79 | 0.64 | 0.04 | 0.12 | 0.62 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.74 | 0.68 | 0.04 | 0.16 | 0.61 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.74 | 0.68 | 0.04 | 0.16 | 0.61 |
| postgres_fdw_federation | 0.78 | 0.76 | 0.74 | 0.63 | 0.62 | 0.10 | 0.35 | 0.58 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.68 | 0.69 | 0.16 | 0.35 | 0.58 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.71 | 0.66 | 0.08 | 0.22 | 0.57 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.73 | 0.61 | 0.04 | 0.18 | 0.57 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.65 | 0.69 | 0.12 | 0.35 | 0.57 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.65 | 0.66 | 0.10 | 0.35 | 0.56 |
| blue_green_upgrade_via_logical_replication | 0.76 | 0.68 | 0.82 | 0.53 | 0.73 | 0.10 | 0.72 | 0.56 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.81 | 0.50 | 0.04 | 0.12 | 0.53 |


## Cited rules
- rule-logical-replication-for-zero-downtime-migrations (contrib 0.82)
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-logical-replication-pair-for-blue-green-upgrade (contrib 0.78)
- rule-postgres-fdw-for-federation (contrib 0.80)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-fdw-federation-for-modernization-bridge (contrib 0.74)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
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
    "foreign_postgres_access",
    "append_only_events"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "postgres_fdw",
      "reason": "Some validation reads must span old PostgreSQL systems during migration."
    }
  ],
  "free_form_notes": "Several PostgreSQL databases and one vendor source are being consolidated. The PostgreSQL systems need publication/subscription migration with validation queries, while FDW is a transition tool for bounded reads. The migration playbook must cover primary keys, sequences, DDL, lag, and rollback.",
  "intake_id": "modernization-multi-database-consolidation",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": true,
    "has_legacy_postgres_source": true,
    "requires_federation_via_fdw": true,
    "requires_zero_downtime_migration": true
  },
  "organization": {
    "industry": "modernization_bridge",
    "managed_service_requirement": "strongly_preferred",
    "operational_tolerance": "medium",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 19
  },
  "scale_signals": {
    "concurrent_connections_peak": 440,
    "growth_rate_month_over_month": 0.06,
    "read_throughput_qps": 1700,
    "row_counts_largest_tables": {
      "accounts": 56000000,
      "audit_events": 260000000,
      "ledger_events": 180000000
    },
    "write_throughput_rows_per_sec": 520
  },
  "security_constraints": [
    "pii_in_scope",
    "audit_required"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "migration_bridge",
    "oltp_heavy",
    "read_heavy",
    "replication_fanout"
  ]
}
```

</details>

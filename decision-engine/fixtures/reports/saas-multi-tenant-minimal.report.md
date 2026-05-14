# PostgreSQL Architecture Recommendation
Intake: saas-multi-tenant-minimal  |  Generated: 2026-05-14T07:36:44.877586Z
Industry: SaaS Multi-tenant  |  Tenancy: multi_tenant_shared_schema  |  Ops tolerance: low

## Summary
The intake points to 3 immediate recommendations, 13 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. No anti-pattern warning matched this intake.

## Recommend now

- **Constraints** — score 0.70
  - Why now: audit_required posture depends on database-enforced state transitions, not only application logging. Relational integrity gives audit reviewers durable evidence that invalid business states were rejected. Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If the audit scope is not yet named, start by identifying which tables and state changes require evidence. If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Add append-only audit tables, actor identity propagation, and retention reviews once regulated workflows are mapped. Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.70 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Row-level Security** — score 0.70
  - Why now: Shared-schema tenancy puts tenant isolation inside every query path. RLS gives the database a backstop when application filters are missed.
  - Why not something else: RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.
  - Triggers for next stage: Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.


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

- **Generated Columns** — score 0.60
  - Why now: Generated columns make repeatedly queried JSONB keys visible to constraints and indexes.
  - Why not something else: Wait until the hot keys are known; generated columns should not mirror every JSON attribute.
  - Triggers for next stage: Promote keys when query traces show stable filters, joins, uniqueness, or validation needs.

- **GIN JSONB Containment** — score 0.59
  - Why now: GIN JSONB can support containment queries on flexible attributes.
  - Why not something else: It is costly when the application does not use containment or filters too broadly.
  - Triggers for next stage: Adopt after EXPLAIN shows repeated @> predicates with selective keys.

- **JSONB** — score 0.58
  - Why now: JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.
  - Why not something else: Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.
  - Triggers for next stage: Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.

- **Physical Replication** — score 0.58
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **PgBouncer** — score 0.57 — [module pgbouncer]
  - Why now: High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.
  - Why not something else: Confirm application compatibility with transaction pooling, prepared statements, and session settings. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Adopt once pool sizing, failover routing, and idle-session behavior are documented.

- **Covering B-tree With INCLUDE** — score 0.57
  - Why now: Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.
  - Why not something else: Covering indexes add write and storage cost, so projections must be stable and valuable.
  - Triggers for next stage: Adopt when visibility map health and EXPLAIN show index-only scan potential.

- **PgBouncer in Front** — score 0.57
  - Why now: Putting PgBouncer in front makes connection admission a topology concern. Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.
  - Why not something else: It cannot compensate for long transactions or inefficient queries. Pool mode can break session-state assumptions and should be tested with the application. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Test failover target changes and pool draining in maintenance runbooks. Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

- **Expression Indexes** — score 0.57
  - Why now: Expression indexes can support normalized lookup while keeping the base model compact.
  - Why not something else: They depend on exact expression matching and should be tied to specific query shapes.
  - Triggers for next stage: Adopt once normalized email, SKU, phone, or JSON extraction filters repeat.

- **Primary With Read Replicas** — score 0.57
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **pgcrypto** — score 0.53 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- No anti-pattern warnings matched.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.72 | 0.04 | 0.06 | 0.70 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.81 | 0.81 | 0.04 | 0.12 | 0.70 |
| row_level_security | 0.92 | 0.88 | 0.90 | 0.70 | 0.72 | 0.04 | 0.25 | 0.70 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.74 | 0.72 | 0.04 | 0.12 | 0.63 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.70 | 0.77 | 0.04 | 0.16 | 0.62 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.70 | 0.77 | 0.04 | 0.16 | 0.62 |
| generated_columns | 0.64 | 0.82 | 0.72 | 0.73 | 0.67 | 0.04 | 0.15 | 0.60 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.67 | 0.66 | 0.04 | 0.22 | 0.59 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.72 | 0.64 | 0.04 | 0.18 | 0.58 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.67 | 0.75 | 0.08 | 0.22 | 0.58 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.64 | 0.78 | 0.24 | 0.35 | 0.57 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.69 | 0.70 | 0.04 | 0.18 | 0.57 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.61 | 0.78 | 0.12 | 0.35 | 0.57 |
| expression_indexes | 0.62 | 0.74 | 0.70 | 0.70 | 0.64 | 0.04 | 0.13 | 0.57 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.61 | 0.75 | 0.10 | 0.35 | 0.57 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.77 | 0.59 | 0.04 | 0.12 | 0.53 |


## Cited rules
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-rls-when-multi-tenant-and-shared-schema (contrib 0.88)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-generated-columns-for-jsonb-hot-keys (contrib 0.66)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)


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
    "semi_structured_jsonb",
    "append_only_events"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "Shared-schema SaaS with strict tenant isolation and limited operations staffing.",
  "intake_id": "saas-multi-tenant-minimal",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "saas_multi_tenant",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds",
      "azure_pg"
    ],
    "team_size_engineers": 12
  },
  "scale_signals": {
    "concurrent_connections_peak": 260,
    "growth_rate_month_over_month": 0.11,
    "largest_object_bytes": 262144,
    "read_throughput_qps": 2400,
    "row_counts_largest_tables": {
      "accounts": 1200000,
      "activities": 45000000
    },
    "write_throughput_rows_per_sec": 180
  },
  "security_constraints": [
    "rls_required",
    "audit_required",
    "pii_in_scope",
    "gdpr_dsr"
  ],
  "tenancy_model": "multi_tenant_shared_schema",
  "workload_patterns": [
    "oltp_heavy",
    "read_heavy",
    "strong_tenant_locality"
  ]
}
```

</details>

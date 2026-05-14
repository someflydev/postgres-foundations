# PostgreSQL Architecture Recommendation
Intake: ecommerce-marketplace-many-sellers  |  Generated: 2026-05-14T07:31:46.247363Z
Industry: Ecommerce Marketplace  |  Tenancy: multi_tenant_shared_schema  |  Ops tolerance: medium

## Summary
The intake points to 5 immediate recommendations, 17 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

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

- **Generated Columns** — score 0.61
  - Why now: Generated columns make repeatedly queried JSONB keys visible to constraints and indexes.
  - Why not something else: Wait until the hot keys are known; generated columns should not mirror every JSON attribute.
  - Triggers for next stage: Promote keys when query traces show stable filters, joins, uniqueness, or validation needs.

- **GIN JSONB Containment** — score 0.60
  - Why now: GIN JSONB can support containment queries on flexible attributes.
  - Why not something else: It is costly when the application does not use containment or filters too broadly.
  - Triggers for next stage: Adopt after EXPLAIN shows repeated @> predicates with selective keys.

- **JSONB** — score 0.60
  - Why now: JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.
  - Why not something else: Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.
  - Triggers for next stage: Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.

- **Materialized Views** — score 0.59
  - Why now: Adjacent analytics often needs precomputed read models before replicas or distributed systems.
  - Why not something else: Refresh cadence, staleness tolerance, and locking behavior must be known first.
  - Triggers for next stage: Adopt when repeated aggregate queries dominate total time and stale-enough answers are acceptable.

- **PgBouncer** — score 0.59 — [module pgbouncer]
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

- **Expression Indexes** — score 0.58
  - Why now: Expression indexes can support normalized lookup while keeping the base model compact.
  - Why not something else: They depend on exact expression matching and should be tied to specific query shapes.
  - Triggers for next stage: Adopt once normalized email, SKU, phone, or JSON extraction filters repeat.

- **pg_partman** — score 0.58 — [module pg-partman]
  - Why now: Recurring time-based partition creation and retention can justify pg_partman automation.
  - Why not something else: The table must already deserve partitioning; pg_partman is not the reason to partition.
  - Triggers for next stage: Adopt when future partition creation or retention jobs become reviewed operational toil.

- **Primary With Read Replicas** — score 0.58
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

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
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.83 | 0.72 | 0.04 | 0.12 | 0.64 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.79 | 0.77 | 0.04 | 0.16 | 0.63 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.79 | 0.77 | 0.04 | 0.16 | 0.63 |
| generated_columns | 0.64 | 0.82 | 0.72 | 0.82 | 0.67 | 0.04 | 0.15 | 0.61 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.76 | 0.66 | 0.04 | 0.22 | 0.60 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.81 | 0.64 | 0.04 | 0.18 | 0.60 |
| materialized_views | 0.66 | 0.66 | 0.74 | 0.82 | 0.71 | 0.04 | 0.16 | 0.59 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.73 | 0.78 | 0.16 | 0.35 | 0.59 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.76 | 0.75 | 0.08 | 0.22 | 0.59 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.78 | 0.70 | 0.04 | 0.18 | 0.59 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.70 | 0.78 | 0.12 | 0.35 | 0.59 |
| expression_indexes | 0.62 | 0.74 | 0.70 | 0.80 | 0.64 | 0.04 | 0.13 | 0.58 |
| pg_partman | 0.64 | 0.82 | 0.74 | 0.64 | 0.85 | 0.20 | 0.38 | 0.58 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.70 | 0.75 | 0.10 | 0.35 | 0.58 |
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
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-generated-columns-for-jsonb-hot-keys (contrib 0.66)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
- rule-materialized-views-for-adjacent-analytics (contrib 0.67)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-pg-partman-when-partitioning-managed-manually (contrib 0.62)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
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
    "semi_structured_jsonb",
    "append_only_events"
  ],
  "existing_postgres_topology": "primary_with_read_replicas",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "Sellers act like tenants, and the team needs a decision on partitioning orders and inventory movement history before holiday volume. Some sellers share fulfillment networks, so tenant locality is strong for dashboards but weaker for shipment allocation. Growth horizon: 6, 12, and 24 months. Restore drills are not documented.",
  "intake_id": "ecommerce-marketplace-many-sellers",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "ecommerce_marketplace",
    "managed_service_requirement": "strongly_preferred",
    "operational_tolerance": "medium",
    "portability_constraints": [
      "aws_rds",
      "any_managed"
    ],
    "team_size_engineers": 38
  },
  "scale_signals": {
    "concurrent_connections_peak": 980,
    "growth_rate_month_over_month": 0.15,
    "read_throughput_qps": 5400,
    "row_counts_largest_tables": {
      "inventory_movements": 190000000,
      "orders": 76000000,
      "seller_events": 130000000
    },
    "write_throughput_rows_per_sec": 980
  },
  "security_constraints": [
    "pii_in_scope",
    "rls_required",
    "audit_required"
  ],
  "tenancy_model": "multi_tenant_shared_schema",
  "workload_patterns": [
    "oltp_heavy",
    "read_heavy",
    "append_heavy",
    "strong_tenant_locality",
    "analytics_adjacent"
  ]
}
```

</details>

# PostgreSQL Architecture Recommendation
Intake: fintech-startup-payments-gateway  |  Generated: 2026-05-13T16:23:17.586868Z
Industry: Fintech Payments  |  Tenancy: single_tenant  |  Ops tolerance: low

## Summary
The intake points to 2 immediate recommendations, 4 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.67
  - Why now: audit_required posture depends on database-enforced state transitions, not only application logging. Relational integrity gives audit reviewers durable evidence that invalid business states were rejected. Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If the audit scope is not yet named, start by identifying which tables and state changes require evidence. If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Add append-only audit tables, actor identity propagation, and retention reviews once regulated workflows are mapped. Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.67 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.


## Candidate later

- **BRIN for Append-only Time** — score 0.60
  - Why now: Append-heavy chronological data often gets useful pruning from small BRIN indexes.
  - Why not something else: BRIN depends on physical correlation and does not replace point-lookup btrees.
  - Triggers for next stage: Adopt when time-window scans dominate and table ordering remains correlated.

- **Partial Indexes** — score 0.58
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.58
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **pgcrypto** — score 0.50 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **partition_too_early**: Append-heavy alone does not justify partitioning when the largest table is still modest.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.36 | 0.04 | 0.06 | 0.67 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.81 | 0.45 | 0.04 | 0.12 | 0.67 |
| brin_append_only_chronological | 0.68 | 0.86 | 0.74 | 0.78 | 0.39 | 0.04 | 0.10 | 0.60 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.70 | 0.41 | 0.04 | 0.16 | 0.58 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.70 | 0.41 | 0.04 | 0.16 | 0.58 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.77 | 0.23 | 0.04 | 0.12 | 0.50 |


## Cited rules
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-brin-for-append-heavy-chronological (contrib 0.70)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-warn-partition-too-early (contrib 0.72)


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
    "append_only_events"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "pgcrypto",
      "reason": "Public references should not expose sequence values."
    }
  ],
  "free_form_notes": "They want immutable ledger checks and better idempotency before any extension discussion; pgcrypto is being considered for public payment references. Reconciliation is still partly spreadsheet-driven, so operational risk comes from human correction loops as much as query speed. Growth horizon: 6, 12, and 24 months. Restore drills are not documented.",
  "intake_id": "fintech-startup-payments-gateway",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "fintech_payments",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 10
  },
  "scale_signals": {
    "concurrent_connections_peak": 120,
    "growth_rate_month_over_month": 0.13,
    "read_throughput_qps": 360,
    "row_counts_largest_tables": {
      "ledger_entries": 2800000,
      "payments": 850000,
      "webhook_events": 4100000
    },
    "write_throughput_rows_per_sec": 95
  },
  "security_constraints": [
    "pci",
    "pii_in_scope",
    "audit_required"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "oltp_heavy",
    "append_heavy"
  ]
}
```

</details>
# PostgreSQL Architecture Recommendation
Intake: saas-early-stage-crm  |  Generated: 2026-05-13T16:52:16.569180Z
Industry: SaaS Multi-tenant  |  Tenancy: multi_tenant_shared_schema  |  Ops tolerance: low

## Summary
The intake points to 3 immediate recommendations, 7 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. No anti-pattern warning matched this intake.

## Recommend now

- **Constraints** — score 0.66
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.66 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Row-level Security** — score 0.66
  - Why now: Shared-schema tenancy puts tenant isolation inside every query path. RLS gives the database a backstop when application filters are missed.
  - Why not something else: RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.
  - Triggers for next stage: Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.


## Candidate later

- **Partial Indexes** — score 0.57
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.57
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **Generated Columns** — score 0.56
  - Why now: Generated columns make repeatedly queried JSONB keys visible to constraints and indexes.
  - Why not something else: Wait until the hot keys are known; generated columns should not mirror every JSON attribute.
  - Triggers for next stage: Promote keys when query traces show stable filters, joins, uniqueness, or validation needs.

- **GIN JSONB Containment** — score 0.54
  - Why now: GIN JSONB can support containment queries on flexible attributes.
  - Why not something else: It is costly when the application does not use containment or filters too broadly.
  - Triggers for next stage: Adopt after EXPLAIN shows repeated @> predicates with selective keys.

- **JSONB** — score 0.54
  - Why now: JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.
  - Why not something else: Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.
  - Triggers for next stage: Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.

- **Expression Indexes** — score 0.53
  - Why now: Expression indexes can support normalized lookup while keeping the base model compact.
  - Why not something else: They depend on exact expression matching and should be tied to specific query shapes.
  - Triggers for next stage: Adopt once normalized email, SKU, phone, or JSON extraction filters repeat.

- **pgcrypto** — score 0.49 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- **pgvector** — score 0.32 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- No anti-pattern warnings matched.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.76 | 0.36 | 0.04 | 0.06 | 0.66 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.75 | 0.45 | 0.04 | 0.12 | 0.66 |
| row_level_security | 0.92 | 0.88 | 0.90 | 0.65 | 0.36 | 0.04 | 0.25 | 0.66 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.64 | 0.41 | 0.04 | 0.16 | 0.57 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.64 | 0.41 | 0.04 | 0.16 | 0.57 |
| generated_columns | 0.64 | 0.82 | 0.72 | 0.67 | 0.31 | 0.04 | 0.15 | 0.56 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.60 | 0.30 | 0.04 | 0.22 | 0.54 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.66 | 0.28 | 0.04 | 0.18 | 0.54 |
| expression_indexes | 0.62 | 0.74 | 0.70 | 0.65 | 0.28 | 0.04 | 0.13 | 0.53 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.71 | 0.23 | 0.04 | 0.12 | 0.49 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.45 | 0.23 | 0.08 | 0.72 | 0.32 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-rls-when-multi-tenant-and-shared-schema (contrib 0.88)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-generated-columns-for-jsonb-hot-keys (contrib 0.66)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
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
    "semi_structured_jsonb"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "pgvector",
      "reason": "Product stakeholders asked whether semantic retrieval belongs in PostgreSQL."
    }
  ],
  "free_form_notes": "They are considering pgvector for account notes because sales managers ask for semantic recall, but the team has not built a lexical search baseline yet. Two design partners use unusually broad custom fields, so JSONB appears in hot screens even though most tenants remain simple. Growth horizon: 6, 12, and 24 months. Restore drills are not documented.",
  "intake_id": "saas-early-stage-crm",
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
      "aws_rds"
    ],
    "team_size_engineers": 8
  },
  "scale_signals": {
    "concurrent_connections_peak": 140,
    "growth_rate_month_over_month": 0.11,
    "read_throughput_qps": 520,
    "row_counts_largest_tables": {
      "accounts": 320000,
      "audit_events": 2200000,
      "tenant_memberships": 180000
    },
    "write_throughput_rows_per_sec": 75
  },
  "security_constraints": [
    "rls_required",
    "pii_in_scope"
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
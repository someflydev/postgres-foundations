# PostgreSQL Architecture Recommendation
Intake: healthcare-clinic-ops-ehr-adjacent  |  Generated: 2026-05-14T10:55:17.529670Z
Industry: Healthcare Operations  |  Tenancy: single_tenant  |  Ops tolerance: low

## Summary
The intake points to 2 immediate recommendations, 10 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. No anti-pattern warning matched this intake.

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

- **Exclusion Constraints** — score 0.61
  - Why now: Scheduling, booking, and availability windows need overlap prevention at write time. Exclusion constraints keep race conditions out of application-only checks.
  - Why not something else: If overlapping rows are allowed by business policy, model the exception first instead of forcing a generic constraint. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Escalate to GiST range indexes and concurrency scenarios when double-booking risk is on a hot path.

- **GiST Range Exclusion** — score 0.60
  - Why now: GiST range indexing supports overlap checks and range predicates for availability data. Range-window workloads need overlap operators and index support.
  - Why not something else: Avoid broad GiST indexes when range predicates are rare or the range column is not selective. Avoid if intervals are rare metadata and not queried or constrained. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Add representative concurrent insert tests before relying on the design. Pair with exclusion constraints for correctness-critical scheduling paths.

- **Partial Indexes** — score 0.58
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.58
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **Generated Columns** — score 0.56
  - Why now: Generated columns make repeatedly queried JSONB keys visible to constraints and indexes.
  - Why not something else: Wait until the hot keys are known; generated columns should not mirror every JSON attribute.
  - Triggers for next stage: Promote keys when query traces show stable filters, joins, uniqueness, or validation needs.

- **GIN JSONB Containment** — score 0.55
  - Why now: GIN JSONB can support containment queries on flexible attributes.
  - Why not something else: It is costly when the application does not use containment or filters too broadly.
  - Triggers for next stage: Adopt after EXPLAIN shows repeated @> predicates with selective keys.

- **JSONB** — score 0.55
  - Why now: JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.
  - Why not something else: Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.
  - Triggers for next stage: Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.

- **Expression Indexes** — score 0.54
  - Why now: Expression indexes can support normalized lookup while keeping the base model compact.
  - Why not something else: They depend on exact expression matching and should be tied to specific query shapes.
  - Triggers for next stage: Adopt once normalized email, SKU, phone, or JSON extraction filters repeat.

- **pgcrypto** — score 0.50 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.

- **PostGIS** — score 0.49 — [module e3-postgis]
  - Why now: The data model already stores geospatial values, so PostGIS should stay on the review path.
  - Why not something else: Coordinates and small zone sets do not justify spatial types and operators until containment, distance, or intersection queries become hot paths.
  - Triggers for next stage: Promote when dispatch, pricing, compliance, or availability depends on indexed spatial predicates rather than display-only coordinates.


## Not enough evidence

- **pgvector** — score 0.33 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- No anti-pattern warnings matched.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.36 | 0.04 | 0.06 | 0.67 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.81 | 0.45 | 0.04 | 0.12 | 0.67 |
| exclusion_constraints | 0.78 | 0.90 | 0.72 | 0.74 | 0.34 | 0.04 | 0.17 | 0.61 |
| gist_range_exclusion | 0.78 | 0.88 | 0.72 | 0.72 | 0.34 | 0.04 | 0.18 | 0.60 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.70 | 0.41 | 0.04 | 0.16 | 0.58 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.70 | 0.41 | 0.04 | 0.16 | 0.58 |
| generated_columns | 0.64 | 0.82 | 0.72 | 0.73 | 0.31 | 0.04 | 0.15 | 0.56 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.67 | 0.30 | 0.04 | 0.22 | 0.55 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.72 | 0.28 | 0.04 | 0.18 | 0.55 |
| expression_indexes | 0.62 | 0.74 | 0.70 | 0.70 | 0.28 | 0.04 | 0.13 | 0.54 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.77 | 0.23 | 0.04 | 0.12 | 0.50 |
| postgis | 0.66 | 0.82 | 0.48 | 0.62 | 0.28 | 0.08 | 0.35 | 0.49 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.51 | 0.23 | 0.08 | 0.72 | 0.33 |


## Cited rules
- rule-audit-required-posture (contrib 0.88)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-exclusion-constraints-for-overlap-windows (contrib 0.82)
- rule-gist-for-range-overlap (contrib 0.76)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-generated-columns-for-jsonb-hot-keys (contrib 0.66)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-postgis-candidate-for-geospatial (contrib 0.62)
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
    "geospatial",
    "ranges_windows",
    "semi_structured_jsonb"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "They need appointment conflict protection and audit trails before considering search or analytics extensions. Clinic locations appear on patient-facing maps, but spatial predicates are not a hot path yet. Some clinics share providers across locations, making simple office-based scheduling rules fail during holiday coverage. Growth horizon: 6, 12, and 24 months. Restore drills are not documented.",
  "intake_id": "healthcare-clinic-ops-ehr-adjacent",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "healthcare_ops",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 9
  },
  "scale_signals": {
    "concurrent_connections_peak": 90,
    "growth_rate_month_over_month": 0.09,
    "read_throughput_qps": 480,
    "row_counts_largest_tables": {
      "appointments": 760000,
      "clinical_notes_metadata": 1200000,
      "patients": 210000
    },
    "write_throughput_rows_per_sec": 70
  },
  "security_constraints": [
    "hipaa",
    "pii_in_scope",
    "audit_required"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "oltp_heavy",
    "read_heavy"
  ]
}
```

</details>
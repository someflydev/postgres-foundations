# PostgreSQL Architecture Recommendation
Intake: logistics-last-mile-single-city  |  Generated: 2026-05-14T07:31:49.272364Z
Industry: Logistics and Geospatial Operations  |  Tenancy: single_tenant  |  Ops tolerance: low

## Summary
The intake points to 2 immediate recommendations, 6 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. No anti-pattern warning matched this intake.

## Recommend now

- **Constraints** — score 0.68
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.68 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.


## Candidate later

- **Exclusion Constraints** — score 0.62
  - Why now: Scheduling, booking, and availability windows need overlap prevention at write time. Exclusion constraints keep race conditions out of application-only checks.
  - Why not something else: If overlapping rows are allowed by business policy, model the exception first instead of forcing a generic constraint. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Escalate to GiST range indexes and concurrency scenarios when double-booking risk is on a hot path.

- **GiST Range Exclusion** — score 0.61
  - Why now: GiST range indexing supports overlap checks and range predicates for availability data. Range-window workloads need overlap operators and index support.
  - Why not something else: Avoid broad GiST indexes when range predicates are rare or the range column is not selective. Avoid if intervals are rare metadata and not queried or constrained. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Add representative concurrent insert tests before relying on the design. Pair with exclusion constraints for correctness-critical scheduling paths.

- **Partial Indexes** — score 0.59
  - Why now: Large OLTP tables often have small hot subsets that should not force full-table index maintenance.
  - Why not something else: Partial indexes need proven predicates; without query traces they become brittle guesses.
  - Triggers for next stage: Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

- **Partial Index for Skew** — score 0.59
  - Why now: The index catalog has a matching pattern for selective predicates on skewed large tables.
  - Why not something else: Wait until the predicate is stable in application SQL and selectivity has been measured.
  - Triggers for next stage: Review index size and write amplification after one representative traffic window.

- **pgcrypto** — score 0.51 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.

- **PostGIS** — score 0.50 — [module e3-postgis]
  - Why now: The data model already stores geospatial values, so PostGIS should stay on the review path.
  - Why not something else: Coordinates and small zone sets do not justify spatial types and operators until containment, distance, or intersection queries become hot paths.
  - Triggers for next stage: Promote when dispatch, pricing, compliance, or availability depends on indexed spatial predicates rather than display-only coordinates.


## Not enough evidence

- **pgvector** — score 0.34 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- No anti-pattern warnings matched.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.76 | 0.55 | 0.04 | 0.06 | 0.68 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.75 | 0.63 | 0.04 | 0.12 | 0.68 |
| exclusion_constraints | 0.78 | 0.90 | 0.72 | 0.68 | 0.52 | 0.04 | 0.17 | 0.62 |
| gist_range_exclusion | 0.78 | 0.88 | 0.72 | 0.66 | 0.52 | 0.04 | 0.18 | 0.61 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.64 | 0.59 | 0.04 | 0.16 | 0.59 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.64 | 0.59 | 0.04 | 0.16 | 0.59 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.71 | 0.41 | 0.04 | 0.12 | 0.51 |
| postgis | 0.66 | 0.82 | 0.48 | 0.56 | 0.46 | 0.08 | 0.35 | 0.50 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.45 | 0.41 | 0.08 | 0.72 | 0.34 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-exclusion-constraints-for-overlap-windows (contrib 0.82)
- rule-gist-for-range-overlap (contrib 0.76)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
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
    "ranges_windows"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "Coordinates support dispatch screens and small service-zone checks, but routing remains in the application. The team is tempted by PostGIS but has not made spatial predicates a hot path; GiST range checks for shift windows matter more today. Restore drills are immature.",
  "intake_id": "logistics-last-mile-single-city",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "logistics_geo",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 7
  },
  "scale_signals": {
    "concurrent_connections_peak": 150,
    "growth_rate_month_over_month": 0.08,
    "read_throughput_qps": 760,
    "row_counts_largest_tables": {
      "deliveries": 2600000,
      "driver_locations": 18000000,
      "service_zones": 48
    },
    "write_throughput_rows_per_sec": 85
  },
  "security_constraints": [
    "pii_in_scope"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "oltp_heavy",
    "read_heavy"
  ]
}
```

</details>

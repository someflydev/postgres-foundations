# PostgreSQL Architecture Recommendation
Intake: ecommerce-dtc-mid-stage  |  Generated: 2026-05-14T10:55:16.611732Z
Industry: Ecommerce Marketplace  |  Tenancy: single_tenant  |  Ops tolerance: low

## Summary
The intake points to 3 immediate recommendations, 17 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **Constraints** — score 0.70
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.70 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Full-text Search** — score 0.67
  - Why now: Document search should first establish lexical parsing, ranking, filters, and explainable relevance.
  - Why not something else: Core FTS may not solve semantic recall, typo tolerance, or multilingual normalization alone.
  - Triggers for next stage: Evaluate pg_trgm for fuzzy lexical misses and pgvector only after lexical baselines plateau.


## Candidate later

- **pg_trgm** — score 0.63 — [module e2-pg-trgm]
  - Why now: Fuzzy lexical matching is the cheapest next step beyond core FTS for typo-tolerant search. pg_trgm is broadly available on managed PostgreSQL.
  - Why not something else: Do not index every text column; scope it to product fields with measured fuzzy-search value. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: If lexical similarity plateaus below product goals, evaluate pgvector for semantic retrieval.

- **GIN Trigram Similarity** — score 0.62
  - Why now: GIN trigram indexes support targeted similarity and substring search paths.
  - Why not something else: Wait until the searched columns and acceptable false-positive rate are known.
  - Triggers for next stage: Adopt after EXPLAIN confirms sequential scans or slow ILIKE paths on target columns.

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

- **Generated Columns** — score 0.59
  - Why now: Generated columns make repeatedly queried JSONB keys visible to constraints and indexes.
  - Why not something else: Wait until the hot keys are known; generated columns should not mirror every JSON attribute.
  - Triggers for next stage: Promote keys when query traces show stable filters, joins, uniqueness, or validation needs.

- **GIN JSONB Containment** — score 0.58
  - Why now: GIN JSONB can support containment queries on flexible attributes.
  - Why not something else: It is costly when the application does not use containment or filters too broadly.
  - Triggers for next stage: Adopt after EXPLAIN shows repeated @> predicates with selective keys.

- **JSONB** — score 0.57
  - Why now: JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.
  - Why not something else: Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.
  - Triggers for next stage: Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.

- **Physical Replication** — score 0.57
  - Why now: Read-heavy systems can isolate reporting and expensive reads with replicas.
  - Why not something else: A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and failover behavior are documented.

- **unaccent** — score 0.57 — [module multi-language-and-unaccent]
  - Why now: Accent folding can improve search recall when multilingual or accent-insensitive matching is intended.
  - Why not something else: It changes text semantics and should not be enabled without product examples.
  - Triggers for next stage: Adopt after representative terms prove accent-insensitive matching improves results.

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

- **Expression Indexes** — score 0.56
  - Why now: Expression indexes can support normalized lookup while keeping the base model compact.
  - Why not something else: They depend on exact expression matching and should be tied to specific query shapes.
  - Triggers for next stage: Adopt once normalized email, SKU, phone, or JSON extraction filters repeat.

- **Primary With Read Replicas** — score 0.56
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.

- **Expression Index for Normalization** — score 0.55
  - Why now: Normalized lookup benefits from matching the indexed expression to application predicates.
  - Why not something else: Expression indexes are fragile when SQL does not consistently use the same expression.
  - Triggers for next stage: Adopt after query review confirms stable lower, unaccent, or extracted-key predicates.

- **pgcrypto** — score 0.52 — [module when-uuid-is-the-right-key]
  - Why now: Database-generated UUID defaults are useful for public identifiers and distributed inserts.
  - Why not something else: Do not treat cryptographic functions as a security architecture without review.
  - Triggers for next stage: Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.


## Not enough evidence

- **pgvector** — score 0.35 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- **jsonb_everything**: The intake language suggests JSONB may be used as a replacement for relational modeling.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.64 | 0.04 | 0.06 | 0.70 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.81 | 0.72 | 0.04 | 0.12 | 0.70 |
| full_text_search | 0.75 | 0.90 | 0.85 | 0.78 | 0.61 | 0.04 | 0.14 | 0.67 |
| pg_trgm | 0.70 | 0.90 | 0.80 | 0.74 | 0.61 | 0.04 | 0.35 | 0.63 |
| gin_trgm_similarity | 0.68 | 0.86 | 0.78 | 0.72 | 0.61 | 0.04 | 0.16 | 0.62 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.74 | 0.64 | 0.04 | 0.12 | 0.62 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.70 | 0.68 | 0.04 | 0.16 | 0.61 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.70 | 0.68 | 0.04 | 0.16 | 0.61 |
| generated_columns | 0.64 | 0.82 | 0.72 | 0.73 | 0.58 | 0.04 | 0.15 | 0.59 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.67 | 0.57 | 0.04 | 0.22 | 0.58 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.72 | 0.55 | 0.04 | 0.18 | 0.57 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.67 | 0.66 | 0.08 | 0.22 | 0.57 |
| unaccent | 0.62 | 0.72 | 0.70 | 0.77 | 0.53 | 0.04 | 0.12 | 0.57 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.64 | 0.69 | 0.24 | 0.35 | 0.56 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.69 | 0.61 | 0.04 | 0.18 | 0.56 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.61 | 0.69 | 0.12 | 0.35 | 0.56 |
| expression_indexes | 0.62 | 0.74 | 0.70 | 0.70 | 0.55 | 0.04 | 0.13 | 0.56 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.61 | 0.66 | 0.10 | 0.35 | 0.56 |
| expression_index_for_normalization | 0.62 | 0.68 | 0.72 | 0.72 | 0.53 | 0.04 | 0.12 | 0.55 |
| pgcrypto | 0.60 | 0.64 | 0.60 | 0.77 | 0.50 | 0.04 | 0.12 | 0.52 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.51 | 0.50 | 0.08 | 0.72 | 0.35 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-full-text-search-before-vector (contrib 0.82)
- rule-pg-trgm-for-fuzzy-support-ui (contrib 0.75)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-generated-columns-for-jsonb-hot-keys (contrib 0.66)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-unaccent-for-search-normalization (contrib 0.62)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
- rule-expression-index-for-normalization (contrib 0.62)
- rule-pgcrypto-for-public-identifiers (contrib 0.58)
- rule-pgvector-not-yet-without-embeddings (contrib 0.56)
- rule-warn-jsonb-everything (contrib 0.78)


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
    "full_text_docs"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [],
  "free_form_notes": "They are considering pg_trgm and unaccent for product search, while resisting a separate search service until PostgreSQL evidence says core search is exhausted. Merchandising teams edit product attributes daily, so JSONB flexibility is useful but the flexible schema pitch cannot become an excuse for everything json storage or unindexed filter chaos. Support also needs case-insensitive email and SKU lookups for order corrections. Growth horizon: 6, 12, and 24 months. Restore drills are not documented.",
  "intake_id": "ecommerce-dtc-mid-stage",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "ecommerce_marketplace",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 14
  },
  "scale_signals": {
    "concurrent_connections_peak": 240,
    "growth_rate_month_over_month": 0.12,
    "read_throughput_qps": 1600,
    "row_counts_largest_tables": {
      "orders": 2200000,
      "products": 180000,
      "search_documents": 620000
    },
    "write_throughput_rows_per_sec": 130
  },
  "security_constraints": [
    "pii_in_scope"
  ],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "oltp_heavy",
    "read_heavy",
    "search_heavy"
  ]
}
```

</details>
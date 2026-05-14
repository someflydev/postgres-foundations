# PostgreSQL Architecture Recommendation
Intake: knowledge-research-corpus-hybrid-retrieval  |  Generated: 2026-05-14T07:31:48.946517Z
Industry: Knowledge and AI Retrieval  |  Tenancy: multi_tenant_shared_schema  |  Ops tolerance: medium

## Summary
The intake points to 6 immediate recommendations, 14 later candidates, and 0 items that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. The warning section calls out 1 anti-pattern that should be handled regardless of scoring.

## Recommend now

- **pgvector** — score 0.72 — [module e4-pgvector]
  - Why now: Embeddings plus semantic retrieval are direct evidence for vector distance search inside PostgreSQL.
  - Why not something else: Keep lexical search, metadata filters, tenant permissions, and deletion behavior in the retrieval plan.
  - Triggers for next stage: Choose HNSW or IVFFlat after recall, latency, memory, and refresh tests are measured.

- **Constraints** — score 0.72
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

- **pg_stat_statements** — score 0.72 — [module e1-pg-stat-statements]
  - Why now: Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions. pg_stat_statements is low-risk and broadly available.
  - Why not something else: Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.
  - Triggers for next stage: Use top total time and calls to justify the next index, schema, or topology recommendation.

- **Row-level Security** — score 0.71
  - Why now: Shared-schema tenancy puts tenant isolation inside every query path. RLS gives the database a backstop when application filters are missed.
  - Why not something else: RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.
  - Triggers for next stage: Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.

- **Full-text Search** — score 0.69
  - Why now: Document search should first establish lexical parsing, ranking, filters, and explainable relevance.
  - Why not something else: Core FTS may not solve semantic recall, typo tolerance, or multilingual normalization alone.
  - Triggers for next stage: Evaluate pg_trgm for fuzzy lexical misses and pgvector only after lexical baselines plateau.

- **pg_trgm** — score 0.65 — [module e2-pg-trgm]
  - Why now: Fuzzy lexical matching is the cheapest next step beyond core FTS for typo-tolerant search. pg_trgm is broadly available on managed PostgreSQL.
  - Why not something else: Do not index every text column; scope it to product fields with measured fuzzy-search value.
  - Triggers for next stage: If lexical similarity plateaus below product goals, evaluate pgvector for semantic retrieval.


## Candidate later

- **GIN Trigram Similarity** — score 0.64
  - Why now: GIN trigram indexes support targeted similarity and substring search paths.
  - Why not something else: Wait until the searched columns and acceptable false-positive rate are known.
  - Triggers for next stage: Adopt after EXPLAIN confirms sequential scans or slow ILIKE paths on target columns.

- **Composite Equality Then Range** — score 0.64
  - Why now: Hot OLTP and read-heavy filters often need equality columns before range or sort columns.
  - Why not something else: Column order must come from real predicates, not generic indexing instinct.
  - Triggers for next stage: Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

- **HNSW Vector ANN** — score 0.64
  - Why now: HNSW is a likely default when recall and latency beat sequential vector scans. HNSW is the likely first ANN candidate for sizeable vector retrieval.
  - Why not something else: Do not build ANN indexes before embedding volume and recall targets are known. It needs memory, recall, build-time, and refresh testing before recommendation-now.
  - Triggers for next stage: Adopt when an offline evaluation set proves recall and p95 latency. Adopt when sequential vector scans miss p95 targets and recall tests pass.

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

- **Primary With Read Replicas** — score 0.58
  - Why now: Reporting or read-heavy traffic may need isolation from primary write latency.
  - Why not something else: Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.
  - Triggers for next stage: Adopt when read routing, lag tolerance, and consistency expectations are explicit.


## Not enough evidence

- No low-confidence recommendation matched.


## Avoid for now

- **no_pooling_high_connections**: High peak connections without pooling evidence risks backend exhaustion and idle-session waste.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| pgvector | 0.94 | 0.98 | 0.96 | 0.69 | 0.85 | 0.10 | 0.72 | 0.72 |
| constraints | 0.86 | 0.90 | 0.82 | 0.91 | 0.72 | 0.04 | 0.06 | 0.72 |
| pg_stat_statements | 0.92 | 0.70 | 0.94 | 0.90 | 0.81 | 0.04 | 0.12 | 0.72 |
| row_level_security | 0.92 | 0.88 | 0.90 | 0.80 | 0.72 | 0.04 | 0.25 | 0.71 |
| full_text_search | 0.75 | 0.90 | 0.85 | 0.87 | 0.70 | 0.04 | 0.14 | 0.69 |
| pg_trgm | 0.70 | 0.90 | 0.80 | 0.83 | 0.70 | 0.04 | 0.35 | 0.65 |
| gin_trgm_similarity | 0.68 | 0.86 | 0.78 | 0.81 | 0.70 | 0.04 | 0.16 | 0.64 |
| btree_composite_equality_then_range | 0.72 | 0.70 | 0.84 | 0.83 | 0.72 | 0.04 | 0.12 | 0.64 |
| hnsw_vector_anns | 0.74 | 0.88 | 0.82 | 0.68 | 0.77 | 0.10 | 0.40 | 0.64 |
| partial_indexes | 0.70 | 0.72 | 0.82 | 0.79 | 0.77 | 0.04 | 0.16 | 0.63 |
| partial_index_for_skew | 0.70 | 0.72 | 0.82 | 0.79 | 0.77 | 0.04 | 0.16 | 0.63 |
| generated_columns | 0.64 | 0.82 | 0.72 | 0.82 | 0.67 | 0.04 | 0.15 | 0.61 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.76 | 0.66 | 0.04 | 0.22 | 0.60 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.81 | 0.64 | 0.04 | 0.18 | 0.60 |
| pgbouncer | 0.76 | 0.62 | 0.82 | 0.73 | 0.78 | 0.16 | 0.35 | 0.59 |
| physical_replication | 0.68 | 0.62 | 0.80 | 0.76 | 0.75 | 0.08 | 0.22 | 0.59 |
| btree_covering_include | 0.62 | 0.66 | 0.78 | 0.78 | 0.70 | 0.04 | 0.18 | 0.59 |
| pgbouncer_in_front | 0.76 | 0.60 | 0.80 | 0.70 | 0.78 | 0.12 | 0.35 | 0.59 |
| expression_indexes | 0.62 | 0.74 | 0.70 | 0.80 | 0.64 | 0.04 | 0.13 | 0.58 |
| primary_with_read_replicas | 0.70 | 0.62 | 0.82 | 0.70 | 0.75 | 0.10 | 0.35 | 0.58 |


## Cited rules
- rule-pgvector-for-semantic-retrieval (contrib 0.78)
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-pg-stat-statements-for-real-workloads (contrib 0.90)
- rule-rls-when-multi-tenant-and-shared-schema (contrib 0.88)
- rule-full-text-search-before-vector (contrib 0.82)
- rule-pg-trgm-for-fuzzy-support-ui (contrib 0.75)
- rule-btree-composite-for-hot-filter-sort (contrib 0.72)
- rule-hnsw-default-for-pgvector (contrib 0.64)
- rule-partial-indexes-for-skewed-hot-sets (contrib 0.68)
- rule-generated-columns-for-jsonb-hot-keys (contrib 0.66)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
- rule-pgbouncer-when-high-concurrency (contrib 0.80)
- rule-physical-replication-for-read-isolation (contrib 0.70)
- rule-btree-covering-for-read-heavy (contrib 0.64)
- rule-pgbouncer-in-front-when-many-short-connections (contrib 0.74)
- rule-read-replica-when-reporting-needs-isolation (contrib 0.70)
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
    "full_text_docs",
    "embeddings_vectors",
    "semi_structured_jsonb"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "pgvector",
      "reason": "Hybrid retrieval has measured semantic recall gaps."
    },
    {
      "extension_slug": "pg_trgm",
      "reason": "Names, gene symbols, and titles need fuzzy lexical recall."
    }
  ],
  "free_form_notes": "Researchers combine project-scoped RLS, lexical ranking, fuzzy title matching, and vector retrieval. The corpus is large enough that ANN index evaluation is required, but HNSW still needs recall and memory gates before it becomes automatic.",
  "intake_id": "knowledge-research-corpus-hybrid-retrieval",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "knowledge_ai",
    "managed_service_requirement": "strongly_preferred",
    "operational_tolerance": "medium",
    "portability_constraints": [
      "aws_rds",
      "azure_pg"
    ],
    "team_size_engineers": 24
  },
  "scale_signals": {
    "concurrent_connections_peak": 620,
    "growth_rate_month_over_month": 0.11,
    "read_throughput_qps": 3600,
    "row_counts_largest_tables": {
      "embedding_rows": 78000000,
      "paper_chunks": 78000000,
      "projects": 180000
    },
    "write_throughput_rows_per_sec": 260
  },
  "security_constraints": [
    "rls_required",
    "pii_in_scope",
    "gdpr_dsr"
  ],
  "tenancy_model": "multi_tenant_shared_schema",
  "workload_patterns": [
    "search_heavy",
    "read_heavy",
    "semantic_retrieval",
    "strong_tenant_locality"
  ]
}
```

</details>

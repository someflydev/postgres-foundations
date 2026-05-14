# PostgreSQL Architecture Recommendation
Intake: knowledge-internal-eng-search  |  Generated: 2026-05-14T07:31:48.332586Z
Industry: Knowledge and AI Retrieval  |  Tenancy: single_tenant  |  Ops tolerance: low

## Summary
The intake points to 1 immediate recommendation, 6 later candidates, and 1 item that need stronger evidence before adoption. The posture stays PostgreSQL core-first: adopt the recommendations with matched data shapes and workload pressure, defer heavier tools until the operating model is clear, and keep portability visible. No anti-pattern warning matched this intake.

## Recommend now

- **Constraints** — score 0.66
  - Why now: Relational core data needs database-enforced truth before optional architecture choices. Constraints make bad states visible across every application writer.
  - Why not something else: If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.
  - Triggers for next stage: Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.


## Candidate later

- **Full-text Search** — score 0.63
  - Why now: Document search should first establish lexical parsing, ranking, filters, and explainable relevance.
  - Why not something else: Core FTS may not solve semantic recall, typo tolerance, or multilingual normalization alone. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: Evaluate pg_trgm for fuzzy lexical misses and pgvector only after lexical baselines plateau.

- **pg_trgm** — score 0.59 — [module e2-pg-trgm]
  - Why now: Fuzzy lexical matching is the cheapest next step beyond core FTS for typo-tolerant search. pg_trgm is broadly available on managed PostgreSQL.
  - Why not something else: Do not index every text column; scope it to product fields with measured fuzzy-search value. The rule matched, but weighted score is below the recommend-now threshold; confirm operational ownership, portability posture, and workload evidence first.
  - Triggers for next stage: If lexical similarity plateaus below product goals, evaluate pgvector for semantic retrieval.

- **GIN Trigram Similarity** — score 0.58
  - Why now: GIN trigram indexes support targeted similarity and substring search paths.
  - Why not something else: Wait until the searched columns and acceptable false-positive rate are known.
  - Triggers for next stage: Adopt after EXPLAIN confirms sequential scans or slow ILIKE paths on target columns.

- **ltree** — score 0.55 — [module ltree]
  - Why now: Hierarchy path search can benefit from native ancestor, descendant, and subtree operators.
  - Why not something else: Recursive CTEs, adjacency lists, or closure tables may be enough for shallow or metadata-rich trees.
  - Triggers for next stage: Adopt when subtree reads or permission-scope path checks are frequent and path labels are stable.

- **GIN JSONB Containment** — score 0.54
  - Why now: GIN JSONB can support containment queries on flexible attributes.
  - Why not something else: It is costly when the application does not use containment or filters too broadly.
  - Triggers for next stage: Adopt after EXPLAIN shows repeated @> predicates with selective keys.

- **JSONB** — score 0.54
  - Why now: JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.
  - Why not something else: Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.
  - Triggers for next stage: Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.


## Not enough evidence

- **pgvector** — score 0.32 — [module e4-pgvector]
  - Why now: The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.
  - Why not something else: There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet. For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.



## Avoid for now

- No anti-pattern warnings matched.



## Score breakdown
| Recommendation | Domain | Data | Workload | Ops | Growth | Portability | Complexity | Total |
| -------------- | ------ | ---- | -------- | --- | ------ | ----------- | ---------- | ----- |
| constraints | 0.86 | 0.90 | 0.82 | 0.82 | 0.28 | 0.04 | 0.06 | 0.66 |
| full_text_search | 0.75 | 0.90 | 0.85 | 0.78 | 0.25 | 0.04 | 0.14 | 0.63 |
| pg_trgm | 0.70 | 0.90 | 0.80 | 0.74 | 0.25 | 0.04 | 0.35 | 0.59 |
| gin_trgm_similarity | 0.68 | 0.86 | 0.78 | 0.72 | 0.25 | 0.04 | 0.16 | 0.58 |
| ltree | 0.70 | 0.86 | 0.72 | 0.66 | 0.21 | 0.05 | 0.35 | 0.55 |
| gin_jsonb_containment | 0.64 | 0.82 | 0.72 | 0.67 | 0.21 | 0.04 | 0.22 | 0.54 |
| jsonb | 0.65 | 0.85 | 0.62 | 0.72 | 0.19 | 0.04 | 0.18 | 0.54 |
| pgvector | 0.45 | 0.40 | 0.50 | 0.51 | 0.14 | 0.08 | 0.72 | 0.32 |


## Cited rules
- rule-prefer-constraints-for-relational-core (contrib 0.86)
- rule-full-text-search-before-vector (contrib 0.82)
- rule-pg-trgm-for-fuzzy-support-ui (contrib 0.75)
- rule-ltree-for-deep-hierarchy (contrib 0.68)
- rule-gin-jsonb-for-containment (contrib 0.66)
- rule-jsonb-hybrid-columns-for-semi-structured (contrib 0.71)
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
    "full_text_docs",
    "semi_structured_jsonb",
    "hierarchy_paths"
  ],
  "existing_postgres_topology": "single_primary",
  "explicit_bias_against": [],
  "explicit_bias_for": [
    {
      "extension_slug": "pg_trgm",
      "reason": "Developers need typo-tolerant fuzzy title and symbol search."
    },
    {
      "extension_slug": "pgvector",
      "reason": "Stakeholders asked for semantic search after lexical launch."
    }
  ],
  "free_form_notes": "The first launch needs core FTS, snippets, filters, typo-tolerant fuzzy matching on titles and symbols, and clear freshness rules. Semantic retrieval is promising later, but there are no embeddings, model owners, or evaluation sets today. Documents also live in stable handbook and service ownership folder paths where subtree search is a normal product behavior. This remains an early search launch rather than a broad read-scaling problem.",
  "intake_id": "knowledge-internal-eng-search",
  "migration_or_federation_needs": {
    "has_legacy_non_postgres_source": false,
    "has_legacy_postgres_source": false,
    "requires_federation_via_fdw": false,
    "requires_zero_downtime_migration": false
  },
  "organization": {
    "industry": "knowledge_ai",
    "managed_service_requirement": "mandatory",
    "operational_tolerance": "low",
    "portability_constraints": [
      "aws_rds"
    ],
    "team_size_engineers": 9
  },
  "scale_signals": {
    "concurrent_connections_peak": 140,
    "growth_rate_month_over_month": 0.07,
    "read_throughput_qps": 900,
    "row_counts_largest_tables": {
      "document_versions": 2400000,
      "documents": 850000,
      "search_events": 9000000
    },
    "write_throughput_rows_per_sec": 65
  },
  "security_constraints": [],
  "tenancy_model": "single_tenant",
  "workload_patterns": [
    "search_heavy"
  ]
}
```

</details>

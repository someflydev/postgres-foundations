# Decision Report: logistics-geo-minimal

- Generated at: `2026-05-12T00:00:00Z`
- Engine version: `0.2.0-prompt42`
- Recommendations: `16`

## Recommendations

### `pg_stat_statements` (extension, recommend_now, 0.90)

Why now:
- Workload decisions need normalized statement evidence before adding indexes, replicas, or extensions.
- pg_stat_statements is low-risk and broadly available.

Why not yet:
- Ownership is still required: reset cadence, query text policy, and review rhythm should be explicit.

Next-stage triggers:
- Use top total time and calls to justify the next index, schema, or topology recommendation.

Sources:
- `rule-pg-stat-statements-for-real-workloads` (0.90)

### `row_level_security` (core_feature, recommend_now, 0.88)

Why now:
- Shared-schema tenancy puts tenant isolation inside every query path.
- RLS gives the database a backstop when application filters are missed.

Why not yet:
- RLS policies need session identity plumbing, bypass-role review, tests, and operational debugging discipline.

Next-stage triggers:
- Review policy coverage for every tenant-scoped table and add plan checks for hot tenant filters.

Sources:
- `rule-rls-when-multi-tenant-and-shared-schema` (0.88)

### `postgis` (extension, recommend_now, 0.88)

Why now:
- Geo-query-heavy workloads need spatial types, predicates, and indexes rather than latitude/longitude conventions.
- PostGIS keeps spatial decisions close to transactional state.

Why not yet:
- PostGIS is not needed for display-only coordinates or rare exports with no spatial predicates.

Next-stage triggers:
- Add geometry validity, coordinate-system rules, and restore validation before production rollout.

Sources:
- `rule-postgis-for-geo-query-heavy` (0.88)

### `constraints` (core_feature, recommend_now, 0.86)

Why now:
- Relational core data needs database-enforced truth before optional architecture choices.
- Constraints make bad states visible across every application writer.

Why not yet:
- If invariants are not yet known, start by naming the entity lifecycle and failure states before adding broad constraints.

Next-stage triggers:
- Escalate to exclusion constraints or RLS when overlap or tenant-isolation rules become explicit.

Sources:
- `rule-prefer-constraints-for-relational-core` (0.86)

### `exclusion_constraints` (core_feature, recommend_now, 0.82)

Why now:
- Scheduling, booking, and availability windows need overlap prevention at write time.
- Exclusion constraints keep race conditions out of application-only checks.

Why not yet:
- If overlapping rows are allowed by business policy, model the exception first instead of forcing a generic constraint.

Next-stage triggers:
- Escalate to GiST range indexes and concurrency scenarios when double-booking risk is on a hot path.

Sources:
- `rule-exclusion-constraints-for-overlap-windows` (0.82)

### `gist_geospatial` (index_pattern, recommend_now, 0.80)

Why now:
- GiST spatial indexes are the expected access path for containment, intersection, and distance predicates.

Why not yet:
- Index choice should wait if the product only stores points for display.

Next-stage triggers:
- Benchmark representative bounding-box and nearest-neighbor queries.

Sources:
- `rule-postgis-for-geo-query-heavy` (0.80)

### `gist_range_exclusion` (index_pattern, recommend_now, 0.78)

Why now:
- GiST range indexing supports overlap checks and range predicates for availability data.
- Range-window workloads need overlap operators and index support.

Why not yet:
- Avoid broad GiST indexes when range predicates are rare or the range column is not selective.
- Avoid if intervals are rare metadata and not queried or constrained.

Next-stage triggers:
- Add representative concurrent insert tests before relying on the design.
- Pair with exclusion constraints for correctness-critical scheduling paths.

Sources:
- `rule-exclusion-constraints-for-overlap-windows` (0.78)
- `rule-gist-for-range-overlap` (0.76)

### `geo_logic_without_postgis` (anti_pattern_warning, avoid_for_now, 0.82)

Why now:
- Geo-heavy logic without PostGIS evidence risks incorrect distance, containment, and indexing behavior.

Why not yet:
- PostGIS can wait for display-only coordinates, but this intake has geo-query-heavy workload signals.

Next-stage triggers:
- Adopt spatial types and validation rules before encoding geometry in ad hoc numeric columns.

Sources:
- `rule-warn-geo-logic-without-postgis` (0.82)

### `btree_composite_equality_then_range` (index_pattern, candidate_later, 0.72)

Why now:
- Hot OLTP and read-heavy filters often need equality columns before range or sort columns.

Why not yet:
- Column order must come from real predicates, not generic indexing instinct.

Next-stage triggers:
- Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

Sources:
- `rule-btree-composite-for-hot-filter-sort` (0.72)

### `physical_replication` (core_feature, candidate_later, 0.70)

Why now:
- Read-heavy systems can isolate reporting and expensive reads with replicas.

Why not yet:
- A replica does not fix bad queries, missing indexes, or write bottlenecks on the primary.

Next-stage triggers:
- Adopt when read routing, lag tolerance, and failover behavior are documented.

Sources:
- `rule-physical-replication-for-read-isolation` (0.70)

### `primary_with_read_replicas` (topology_pattern, candidate_later, 0.70)

Why now:
- Reporting or read-heavy traffic may need isolation from primary write latency.

Why not yet:
- Replicas inherit bad query plans and introduce lag; they are not a first fix for missing indexes.

Next-stage triggers:
- Adopt when read routing, lag tolerance, and consistency expectations are explicit.

Sources:
- `rule-read-replica-when-reporting-needs-isolation` (0.70)

### `partial_indexes` (core_feature, candidate_later, 0.68)

Why now:
- Large OLTP tables often have small hot subsets that should not force full-table index maintenance.

Why not yet:
- Partial indexes need proven predicates; without query traces they become brittle guesses.

Next-stage triggers:
- Adopt when pg_stat_statements or EXPLAIN shows repeated filters on status, tenant, active windows, or sparse flags.

Sources:
- `rule-partial-indexes-for-skewed-hot-sets` (0.68)

### `partial_index_for_skew` (index_pattern, candidate_later, 0.68)

Why now:
- The index catalog has a matching pattern for selective predicates on skewed large tables.

Why not yet:
- Wait until the predicate is stable in application SQL and selectivity has been measured.

Next-stage triggers:
- Review index size and write amplification after one representative traffic window.

Sources:
- `rule-partial-indexes-for-skewed-hot-sets` (0.68)

### `btree_covering_include` (index_pattern, candidate_later, 0.64)

Why now:
- Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.

Why not yet:
- Covering indexes add write and storage cost, so projections must be stable and valuable.

Next-stage triggers:
- Adopt when visibility map health and EXPLAIN show index-only scan potential.

Sources:
- `rule-btree-covering-for-read-heavy` (0.64)

### `pgcrypto` (extension, candidate_later, 0.58)

Why now:
- Database-generated UUID defaults are useful for public identifiers and distributed inserts.

Why not yet:
- Do not treat cryptographic functions as a security architecture without review.

Next-stage triggers:
- Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.

Sources:
- `rule-pgcrypto-for-public-identifiers` (0.58)

### `pgvector` (extension, not_enough_evidence, 0.56)

Why now:
- The intake mentions semantic or vector-style search, so pgvector should stay visible as a possible later option.

Why not yet:
- There is no embeddings_vectors data shape, embedding refresh plan, recall target, or permission-aware retrieval design yet.
- For geo-heavy logistics, PostGIS answers spatial distance and containment questions more directly than vector search.

Next-stage triggers:
- Revisit pgvector after an embedding corpus, offline evaluation set, and lexical or spatial baseline gaps are documented.

Sources:
- `rule-pgvector-not-yet-without-embeddings` (0.56)


## Score Breakdown

- `domain_fit`: 0.72
- `data_shape_fit`: 0.76
- `workload_fit`: 0.78
- `operational_feasibility`: 0.78
- `growth_urgency`: 0.46
- `portability_penalty`: 0.04
- `complexity_penalty`: 0.19

## Warnings

- `geo_logic_without_postgis`: Geo-heavy logic without PostGIS evidence risks incorrect distance, containment, and indexing behavior.

## Followup Questions

No followup questions yet.

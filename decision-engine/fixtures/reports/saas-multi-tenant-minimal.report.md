# Decision Report: saas-multi-tenant-minimal

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

### `pgbouncer` (extension, recommend_now, 0.80)

Why now:
- High peak connections on OLTP/read-heavy traffic should not map one application worker to one backend.

Why not yet:
- Confirm application compatibility with transaction pooling, prepared statements, and session settings.

Next-stage triggers:
- Adopt once pool sizing, failover routing, and idle-session behavior are documented.

Sources:
- `rule-pgbouncer-when-high-concurrency` (0.80)

### `pgbouncer_in_front` (topology_pattern, recommend_now, 0.76)

Why now:
- Putting PgBouncer in front makes connection admission a topology concern.
- Many concurrent sessions call for an explicit pooling layer in front of PostgreSQL.

Why not yet:
- It cannot compensate for long transactions or inefficient queries.
- Pool mode can break session-state assumptions and should be tested with the application.

Next-stage triggers:
- Test failover target changes and pool draining in maintenance runbooks.
- Adopt after transaction duration, idle sessions, and prepared-statement behavior are measured.

Sources:
- `rule-pgbouncer-when-high-concurrency` (0.76)
- `rule-pgbouncer-in-front-when-many-short-connections` (0.74)

### `btree_composite_equality_then_range` (index_pattern, candidate_later, 0.72)

Why now:
- Hot OLTP and read-heavy filters often need equality columns before range or sort columns.

Why not yet:
- Column order must come from real predicates, not generic indexing instinct.

Next-stage triggers:
- Adopt after pg_stat_statements identifies repeated tenant/status/time or account/time access paths.

Sources:
- `rule-btree-composite-for-hot-filter-sort` (0.72)

### `jsonb` (core_feature, candidate_later, 0.71)

Why now:
- JSONB can carry variable attributes while stable identifiers and lifecycle columns stay relational.

Why not yet:
- Do not make the whole entity JSONB when keys are frequently filtered, joined, constrained, or audited.

Next-stage triggers:
- Promote hot JSON keys to generated or ordinary columns once query pressure and invariants are visible.

Sources:
- `rule-jsonb-hybrid-columns-for-semi-structured` (0.71)

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

### `generated_columns` (core_feature, candidate_later, 0.66)

Why now:
- Generated columns make repeatedly queried JSONB keys visible to constraints and indexes.

Why not yet:
- Wait until the hot keys are known; generated columns should not mirror every JSON attribute.

Next-stage triggers:
- Promote keys when query traces show stable filters, joins, uniqueness, or validation needs.

Sources:
- `rule-generated-columns-for-jsonb-hot-keys` (0.66)

### `gin_jsonb_containment` (index_pattern, candidate_later, 0.66)

Why now:
- GIN JSONB can support containment queries on flexible attributes.

Why not yet:
- It is costly when the application does not use containment or filters too broadly.

Next-stage triggers:
- Adopt after EXPLAIN shows repeated @> predicates with selective keys.

Sources:
- `rule-gin-jsonb-for-containment` (0.66)

### `btree_covering_include` (index_pattern, candidate_later, 0.64)

Why now:
- Read-heavy stable projections may benefit from INCLUDE columns and index-only scans.

Why not yet:
- Covering indexes add write and storage cost, so projections must be stable and valuable.

Next-stage triggers:
- Adopt when visibility map health and EXPLAIN show index-only scan potential.

Sources:
- `rule-btree-covering-for-read-heavy` (0.64)

### `expression_indexes` (core_feature, candidate_later, 0.61)

Why now:
- Expression indexes can support normalized lookup while keeping the base model compact.

Why not yet:
- They depend on exact expression matching and should be tied to specific query shapes.

Next-stage triggers:
- Adopt once normalized email, SKU, phone, or JSON extraction filters repeat.

Sources:
- `rule-generated-columns-for-jsonb-hot-keys` (0.61)

### `pgcrypto` (extension, candidate_later, 0.58)

Why now:
- Database-generated UUID defaults are useful for public identifiers and distributed inserts.

Why not yet:
- Do not treat cryptographic functions as a security architecture without review.

Next-stage triggers:
- Adopt when URL-safe identifiers or database-side UUID defaults are explicit requirements.

Sources:
- `rule-pgcrypto-for-public-identifiers` (0.58)


## Score Breakdown

- `domain_fit`: 0.71
- `data_shape_fit`: 0.71
- `workload_fit`: 0.77
- `operational_feasibility`: 0.77
- `growth_urgency`: 0.48
- `portability_penalty`: 0.05
- `complexity_penalty`: 0.18

## Warnings

No warnings.

## Followup Questions

No followup questions yet.

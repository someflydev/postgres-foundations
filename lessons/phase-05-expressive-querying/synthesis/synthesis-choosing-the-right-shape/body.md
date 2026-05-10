# Synthesis: Choosing the Right Shape

## Problem Framing

Expressive SQL is the point where a learner stops treating a query as a single flat SELECT and starts treating it as a shaped explanation. The relational foundation still matters: rows have grain, joins can multiply facts, NULL changes logic, and constraints describe the world. Phase 5 adds query forms that let those facts be staged, compared, reused, ranked, traversed, and defended without leaving PostgreSQL. The goal is not clever syntax. The goal is to make a complicated operational question readable enough that a teammate can review it, adjust it, and trust its edge cases.

This lesson focuses on `cte`, `window_function`, `lateral_join`, `upsert`, `view`, `materialized_view`, `exists`. The examples use the Phase 5 domain packs, where ecommerce has thousands of orders, scheduling has dense appointment history, SaaS has many tenants and usage events, and event-heavy operations has enough rows that grouping and per-source queries feel real. The larger volume is intentional. A window function over three rows is syntactically valid, but it does not teach why partitions, ordering, frames, and per-group subqueries matter in reporting work.

## Minimal Concept Introduction

Use the new query shape when it names a real intermediate idea. A CTE should usually name a business grain such as monthly revenue or eligible customers. A window function should keep row detail while adding context such as rank, running total, prior event, or partition count. A lateral join should be reserved for a right-hand query that depends on each row from the left side. A view should package a stable interface for reuse. A materialized view should be chosen only when the cost and staleness tradeoff have been made explicit.

PostgreSQL will execute many equivalent-looking queries with the same result, but equivalence is not only visual. NULL behavior, duplicate rows, frame defaults, row order, and refresh timing can all change results. Phase 5 therefore treats expressive SQL as an accountability skill: write the query, explain the grain, state whether ordering matters, and identify which rows are intentionally included or excluded.

## Worked Example

The following worked example is intentionally small enough to read and large enough to return non-trivial output against the Phase 5 seed data:

```sql
WITH tenant_usage AS (
    SELECT tenant_id, date_trunc('day', occurred_at)::date AS usage_date, count(*) AS events
    FROM saas.usage_events
    GROUP BY tenant_id, date_trunc('day', occurred_at)::date
)
SELECT t.slug, u.usage_date, u.events,
       rank() OVER (PARTITION BY u.usage_date ORDER BY u.events DESC) AS daily_rank
FROM tenant_usage u
JOIN saas.tenants t ON t.id = u.tenant_id
ORDER BY u.usage_date, daily_rank, t.slug
LIMIT 40;
```

Read the query from the outside in, then from the data grain upward. Ask what one output row represents. Ask which table contributes that row. Ask whether rows can duplicate because of a join, whether NULLs can change the predicate, and whether the final ORDER BY is part of the result contract. If the query uses a staged expression, each stage should have a name that can survive code review. If the query ranks or compares rows, the partition and ordering columns should match the business question rather than merely making PostgreSQL accept the syntax.

## Diagnostic Questions

What is the grain of the final result? Which intermediate grain is named or implied? Does the query keep row detail while adding context, or does it collapse rows through aggregation? If two rows have the same timestamp or amount, is the tie behavior deterministic? If a correlated expression appears, does it run once per outer row conceptually, and is that exactly what the question needs? If the answer will be checked by the exercise runner, should the exercise use `output_comparison: ordered` because the order is part of the answer?

## Common Pitfalls

The most common failure is writing expressive SQL that hides rather than clarifies the logic. A chain of CTEs with vague names is not better than one clear subquery. A window function without a careful frame can look correct while reporting a plateau or jump at tied values. A lateral join can be elegant for per-row top-N work, but it can also conceal a row-by-row query that should have been a set-oriented window solution. A view can make shared SQL easier to maintain, but it does not automatically make a query faster. A materialized view can make repeated aggregates cheaper, but it creates an operational promise to refresh it.

Another failure is using future-phase concepts as a shortcut. Do not turn this lesson into an indexing lesson, a concurrency lesson, or a partitioning lesson. You may notice that some queries would benefit from physical design later. For now, keep the explanation centered on result shape, correctness, and readability. Performance measurement is allowed as a soft observation through `--timing`, but plan analysis and index design arrive later.

## Explain It Back

Explain this query shape to another learner by naming the problem it solves, the row grain it preserves or creates, and the reason the chosen shape is preferable to a simpler SELECT. Then give one case where you would not use it. A strong answer does not recite syntax; it says what the database is being asked to prove. It also identifies the operational boundary: whether the result is always current, whether the order is deterministic, and whether a future maintainer can modify one stage without breaking another stage by accident.

## References and Further Reading

- `docs/glossary.md` defines the Phase 5 vocabulary used in this lesson.
- `docs/expressive-sql-style.md` gives team-scale guidance for choosing between CTEs, subqueries, views, lateral joins, window functions, and materialized views.
- `docs/doctrine.md` explains why PostgreSQL core features are preferred before extension-specific designs.

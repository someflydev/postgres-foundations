# Distinct And Count Distinct Level C 1

## Setup

Seed the Phase 2 saas_multi_tenant pack and open the PostgreSQL lab.

## Given

Relevant tables: saas.tenants, saas.users.

## Task

Write the reference query for `DISTINCT and COUNT DISTINCT`. Keep the output small and ordered when the prompt asks for a predictable row set.

## Allowed concepts

Use Phase 2 joins, keys, GROUP BY, aggregates, HAVING, DISTINCT, and COUNT DISTINCT as needed.

## Not yet allowed

Do not use CTEs, window functions, lateral joins, recursive queries, upserts, views, materialized views, JSONB, arrays, or correlated subqueries.

## Success criteria

- The SQL runs cleanly against the Phase 2 seed pack.
- The returned rows and columns match the requested grain.
- The query uses only the named tables and Phase 2 concepts.

## Oral defense

- Why did you choose this join type?
- What would change if the relationship had zero matching child rows?

Estimated time: 25 minutes.

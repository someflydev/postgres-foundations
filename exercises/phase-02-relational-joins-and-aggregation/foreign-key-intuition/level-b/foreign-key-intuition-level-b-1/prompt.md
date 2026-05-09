# Foreign Key Intuition Level B 1

## Setup

Seed the Phase 2 ecommerce pack and open the PostgreSQL lab.

## Given

Relevant tables: ecommerce.customers, ecommerce.orders.

## Task

Write the reference query for `Foreign Key Intuition`. Keep the output small and ordered when the prompt asks for a predictable row set.

## Allowed concepts

Use Phase 2 joins, keys, GROUP BY, aggregates, HAVING, DISTINCT, and COUNT DISTINCT as needed.

## Not yet allowed

Do not use CTEs, window functions, lateral joins, recursive queries, upserts, views, materialized views, JSONB, arrays, or correlated subqueries.

## Success criteria

- The SQL runs cleanly against the Phase 2 seed pack.
- The returned rows and columns match the requested grain.
- The query uses only the named tables and Phase 2 concepts.

## Hints

- Start by naming the table grain.
- Follow primary key to foreign key relationships in the ON clause.

Estimated time: 15 minutes.

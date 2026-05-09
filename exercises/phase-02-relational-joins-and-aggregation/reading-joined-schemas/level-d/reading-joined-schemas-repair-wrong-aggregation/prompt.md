# Reading Joined Schemas Repair Wrong Aggregation

## Setup

Seed the Phase 2 scheduling pack and open the PostgreSQL lab.

## Given

The broken review query for `Reading Joined Schemas` has a wrong aggregation or missing rows problem. It may also hide duplicates, produce an incorrect count, or select non-aggregated selected columns at the wrong grain.

## Task

Repair the query so it returns the correct row set using only Phase 2 concepts. Explain why the original query was wrong and why the repair preserves the intended grain.

## Allowed concepts

Use joins, primary keys, foreign keys, GROUP BY, aggregates, HAVING, DISTINCT, and COUNT DISTINCT.

## Not yet allowed

Do not use CTEs, window functions, lateral joins, recursive queries, upserts, views, materialized views, JSONB, arrays, or correlated subqueries.

## Success criteria

- The SQL runs cleanly against the Phase 2 seed pack.
- The repaired row set has the correct grain.
- The explanation names the duplicates, incorrect count, missing rows, or wrong aggregation defect.

## Oral defense

- What row did the broken query accidentally duplicate or drop?
- What would break if the join type changed?
- How did your GROUP BY columns match the selected non-aggregated columns?

Estimated time: 35 minutes.

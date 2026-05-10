# Expressive SQL Style

Prefer a CTE when the intermediate result has a name the team would use in a design review: eligible customers, monthly revenue, ranked appointments, or source-hour event counts. A CTE is not automatically clearer; a one-line subquery can be better when the logic is local and naming it would add noise. In PostgreSQL 12 and later, ordinary CTEs may be inlined, while `MATERIALIZED` and `NOT MATERIALIZED` let authors document intent when that distinction matters.

Prefer a subquery when the expression is tightly bound to one predicate or one SELECT-list calculation. Prefer `EXISTS` or `NOT EXISTS` when the question is about presence rather than a value list, especially when NULLs would make `IN` or `NOT IN` harder to reason about.

Use `LATERAL` when each outer row needs its own small query, such as a per-customer top-N report or the latest usage event per tenant. Use a window function when the problem is naturally set-wide and you want to keep row detail while adding rank, previous-row values, running totals, or partition counts.

Use a view to give a stable name to shared SQL, hide incidental join detail, or support a permission boundary in a later security phase. Do not present a regular view as a performance tool; it is a reusable query interface.

Use a materialized view only when the team accepts staleness and owns the refresh policy. Document what refreshes it, how often, whether concurrent refresh is required, and what users should do when freshness matters more than speed.

# First SELECT: Write Query

Seed pack: `scheduling`, phase `1`.

Write the query independently against `scheduling.providers`. Do not look at `solution.sql` until after you have made an attempt. The expected result is one row for Dr. Rivera with display_name and specialty.

Work against `scheduling.providers` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `scheduling` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `scheduling.providers`.
- The answer ends with a semicolon.

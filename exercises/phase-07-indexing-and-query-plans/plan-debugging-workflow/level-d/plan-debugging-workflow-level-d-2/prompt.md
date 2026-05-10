# Plan Debugging Workflow Level D2

The plan has a severe estimated-vs-actual row mismatch on correlated columns.
Use `EXPLAIN ANALYZE BUFFERS` to identify the mismatch, then propose the
smallest repair: `ANALYZE`, extended statistics with `CREATE STATISTICS`, or a
query rewrite that makes the relationship visible to the planner.

Record the before and after plan and explain the maintenance tradeoff.

# Solution

The full index on `status` is weak because the value has low selectivity in the phase 7a data. A broad query that keeps a large fraction of `orders` can be cheaper as a sequential scan than as an index walk plus many heap visits. The extra index still adds write amplification: inserts and status updates maintain one more B-tree, and vacuum has more index pages to consider.

The Phase 7b direction is a partial index tied to a genuinely narrow status predicate, for example a hot query on only pending orders. Do not keep the broad status index unless `pg_stat_statements` and `EXPLAIN (ANALYZE, BUFFERS)` show it pays for its maintenance cost.

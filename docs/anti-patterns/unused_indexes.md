# Unused Indexes

An unused index is not free. It consumes storage, slows writes, creates vacuum
work, and can distract plan reviews.

Start with `pg_stat_user_indexes`:

```sql
SELECT schemaname, relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, relname, indexrelname;
```

Treat this as evidence, not an automatic drop list. A rarely used unique index
may enforce a business invariant. A seasonal report index may be quiet for
months. A new index may not have lived through enough workload.

Before dropping, identify the query the index was supposed to serve, check
constraint ownership, inspect recent deployment history, and measure write
pressure. Drop only when the index has no correctness role and no observed or
credible workload.

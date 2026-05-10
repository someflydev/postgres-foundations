# Redundant Indexes

Redundant indexes overlap so much that one index can serve the workload of
another. The common case is a left-prefix duplicate:

```sql
CREATE INDEX orders_customer_idx ON ecommerce.orders (customer_id);
CREATE INDEX orders_customer_placed_idx ON ecommerce.orders (customer_id, placed_at);
```

The second index can often serve predicates on `customer_id` alone, so the
first may be unnecessary. The answer still depends on sort direction, included
columns, uniqueness, index size, and write cost.

Look for indexes on the same table with identical leading columns, duplicated
expressions, or broad indexes that fully cover narrower ones. Then verify with
real query plans. Do not drop an index only because it looks similar; prove
that the surviving index supports the important predicates and ordering
requirements.

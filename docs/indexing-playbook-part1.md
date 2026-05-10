# Indexing Playbook Part 1

Part 1 covers the Phase 7a surface: scans, B-tree indexes, and composite
indexes. Part 2 extends this with partial, expression, GIN, GiST, BRIN, and
deeper plan interpretation.

## Start With the Query Pattern

Write the query pattern before writing the index:

```text
table: ecommerce.orders
predicate: customer_id = ?
ordering: placed_at DESC
limit: 20
payload: id, order_number, placed_at, total_amount
candidate: (customer_id, placed_at DESC)
```

If the query pattern is vague, the index is probably vague too.

## Sequential Scans

A sequential scan reads table pages and tests visible rows. It is often correct
when the predicate keeps a large fraction of the table, the table is small, or
the query must aggregate broad history. Do not treat `Seq Scan` as an automatic
bug.

Useful checks:

- estimated rows versus actual rows
- shared blocks hit and read
- rows removed by filter
- whether a narrower predicate exists in the real workload

## B-tree Basics

B-tree is PostgreSQL's default index method for equality and ordered scalar
comparisons. It is the first candidate for:

- primary-key and natural-key lookups
- equality predicates on selective columns
- range predicates on ordered values
- `ORDER BY ... LIMIT` when the index order matches the query

Low-cardinality columns such as a three-value `status` column usually need more
evidence before they deserve a full index.

## Composite Indexes

For `(a, b, c)`, PostgreSQL can use the leading key sequence: `a`, then `a,b`,
then `a,b,c`. It usually cannot enter the B-tree efficiently from `b` alone.

Practical ordering rule:

```text
equality predicates first, range predicate next, ordering requirement last when it still matches
```

Example:

```sql
CREATE INDEX orders_customer_placed_at_idx
ON ecommerce.orders (customer_id, placed_at DESC);
```

This serves recent orders for one customer. It is not the same as:

```sql
CREATE INDEX orders_placed_at_customer_idx
ON ecommerce.orders (placed_at DESC, customer_id);
```

The second index enters by time first, so it may scan many recent orders before
finding one customer's rows.

## Covering Indexes

Use `INCLUDE` for payload columns that are returned but not searched:

```sql
CREATE INDEX orders_customer_recent_covering_idx
ON ecommerce.orders (customer_id, placed_at DESC)
INCLUDE (order_number, total_amount);
```

This can enable an index-only scan, but only when visibility map conditions
allow PostgreSQL to avoid heap fetches. The cost is a larger index and more
write work.

## Measurement Loop

1. Capture the baseline:

   ```bash
   uv run pgfound lab explain --baseline pre starter.sql
   ```

2. Add the candidate index.

3. Capture and compare:

   ```bash
   uv run pgfound lab explain --baseline post --compare pre starter.sql
   ```

4. Explain the result in terms of access path, rows, buffers, and write cost.

## Removal Is Part of Index Design

An index that no longer serves a real workload should be removed. Watch for
redundant prefixes, broad low-selectivity indexes, and indexes created for one
experiment that stayed behind. Every index increases insert, update, delete,
vacuum, and storage pressure.

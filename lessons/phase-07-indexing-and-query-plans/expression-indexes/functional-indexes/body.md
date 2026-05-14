# Functional Indexes

## Problem Framing

Functional indexes, often called expression indexes, are for queries that repeatedly filter or sort by a derived value rather than the stored column value. They are powerful when the expression is stable, deterministic for the query's purpose, and used consistently. They are fragile when application paths normalize data in different ways. This lesson uses `lower(email)` and `date_trunc` because they show both sides: normalized lookup and time bucketing.

The key question is whether the expression is part of the data access contract. If the application always finds a customer by case-insensitive email, an index on raw `email` does not match the predicate. If daily reporting groups orders by the day of `placed_at`, an index on the timestamp may not help the expression predicate unless the query can use a range on the raw timestamp or an expression index that exactly matches the expression.

## Minimal Concept Introduction

A B-tree expression index stores the result of an expression for each row. PostgreSQL can use it when the query applies the same expression in a way the planner recognizes. The expression must be immutable or stable enough for the index definition PostgreSQL accepts. More importantly, the team must standardize the query pattern. `lower(email) = lower($1)` and `email ILIKE $1` are not the same access path. `date_trunc('day', placed_at)` and a half-open timestamp range are also different designs.

Expression indexes can be a bridge between ideal modeling and real workload pressure. They can protect a legacy email column that was not normalized on write. They can speed a report while the team decides whether a generated column would make the derived value more explicit. They should not hide inconsistent application rules forever.

## Worked Example

Worked example anchor: case-insensitive-customer-email

A support tool needs to find customers by email regardless of case:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email, created_at
FROM ecommerce.customers
WHERE lower(email) = lower('Ada@example.com');
```

A normal index on `email` cannot satisfy `lower(email)`. The matching index is on the expression:

```sql
CREATE INDEX customers_lower_email_idx
ON ecommerce.customers (lower(email));
ANALYZE ecommerce.customers;
```

After the change, verify that the plan uses the expression index and that actual rows match expectations. Then check every application path that performs email lookup. If one path uses `lower(email)` and another uses `email ILIKE`, the index will not reliably serve both. The right long-term fix may be a canonicalized email column or a generated column with a uniqueness constraint, but the expression index is a valid measured step when the existing table is already in production.

A reporting example has a different tradeoff:

```sql
CREATE INDEX orders_order_day_idx
ON ecommerce.orders (date_trunc('day', placed_at));
```

This can help a query that filters on `date_trunc('day', placed_at)`, but a half-open range such as `placed_at >= DATE '2026-05-01' AND placed_at < DATE '2026-05-02'` may use a normal timestamp index and avoid expression fragility. The learner must defend which query shape the system will standardize.

## Diagnostic Questions

Ask whether the expression appears in the actual predicate, not only in a report title. Ask whether the expression is deterministic for the business rule. Ask whether a generated column would make the rule clearer. Ask whether a normal range predicate could avoid the expression index. Ask how many writes now maintain the derived value and whether the query volume justifies it. For date buckets, ask about time zone rules before indexing `date_trunc`; a day in UTC may not be the day the business means.

## Common Pitfalls

The common failure is adding an expression index and then writing a different expression in production. Another failure is indexing a convenience expression that should be materialized as a real invariant, such as a normalized SKU that must be unique. For time expressions, the pitfall is mixing local time and UTC without saying which one the index represents. For JSONB extraction expressions, the pitfall is pretending an expression index on one key is the same as a GIN index for containment; those are different operator families and different maintenance costs.

## Explain It Back

A strong explanation says: "The query predicate is `lower(email) = lower($1)`, so a raw email index does not match. The expression index stores `lower(email)` and lets the planner seek the normalized value. I would standardize all case-insensitive lookup SQL on this expression, verify buffers and actual rows with EXPLAIN ANALYZE, and consider a generated normalized email column if this becomes a core identity invariant." That explanation connects the expression, the query, and the operational maintenance cost.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` for expression index checks and `docs/constraints-cookbook.md` when the derived value should become an enforced data invariant.

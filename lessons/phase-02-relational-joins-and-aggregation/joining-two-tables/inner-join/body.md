# Inner Join

## Problem Framing

Phase 2 starts from a practical problem: one table is no longer enough to answer normal product questions. A customer can place many orders, an order can have many item rows, a provider can have many appointments, and an account can have many users. The first skill is not memorizing join syntax. The first skill is naming the grain of each table before the query is written. A customer row is one customer. An order row is one order. An item row is one product on one order. If those grains are mixed carelessly, PostgreSQL will still return rows, but the answer can be silently wrong.

This lesson focuses on inner join. Keep the question small and concrete. Identify the table that owns the row you need to keep, identify the related table that adds facts, and then choose the SQL shape that preserves the requested grain. In the lab, you can inspect the relevant tables with `\d ecommerce.orders`, `\d ecommerce.order_items`, `\d scheduling.appointments`, or the matching table in the SaaS schema. The table definitions show the primary-key columns and the columns that reference another table. Those references are the map you follow when a query crosses table boundaries.

## Minimal Concept Introduction

A primary key identifies one row inside its table. A foreign key stores a value that must match a referenced key in another table. Together they create a relationship the database can check. In a one-to-many relationship, the parent row appears once, while the child table can hold zero, one, or many matching rows. Joins use those key columns to combine related rows in a result set. Aggregates then summarize result rows, but only after the join and filter steps have shaped the row set.

The important operational habit is to ask, "What does one output row represent?" If one output row represents a customer, group by customer columns and count or sum child rows carefully. If one output row represents an order, do not group only by customer. If missing child rows should still appear, use a left join from the kept side. If only matched facts are relevant, an inner join is usually clearer.

## Worked Example

Run this against the Phase 2 ecommerce seed pack:

```sql
SELECT o.order_number, c.email FROM ecommerce.orders o INNER JOIN ecommerce.customers c ON c.id = o.customer_id ORDER BY o.order_number;
```

Sample output:

```text
 order_number | email
--------------+-------------------
 EC-1001      | ada@example.com
 EC-1002      | grace@example.com
```

Read the output with grain in mind. The selected columns do not merely decorate the result; they tell you what each row means. When the query includes `GROUP BY`, every non-aggregated selected column must belong to the group. When the query includes a join, the `ON` clause should follow a declared relationship, usually a foreign key to a primary key. When the result includes a count, ask whether the count is counting parent rows, child rows, or unique related rows.

## Diagnostic Questions

Before running the query, predict the kept side and the row count. Which table can contribute NULL values after an outer join? Which table can multiply rows because it has several children for one parent? If the query groups rows, name the grain out loud before reading the aggregate. If a query uses `HAVING`, check that it is filtering groups after aggregation, not trying to replace a normal row-level `WHERE` predicate.

After running the query, compare the output to a tiny manual check. For ecommerce, look at one order and its item rows. For scheduling, look at one provider and the appointments attached to that provider. For SaaS, look at one account and the users attached to it. A correct Phase 2 answer should be explainable from those small facts without relying on hidden database behavior.

## Common Pitfalls

The most common mistake is grouping at one grain while selecting columns from another. PostgreSQL often rejects that with a non-aggregated-column error, which is useful feedback. A more dangerous mistake is a wrong aggregation that runs: for example, summing order totals after joining to order items duplicates the order total once per item row. Another common mistake is using an inner join for a report that must include parents with zero children. That query looks clean but creates missing rows.

Avoid solving these mistakes with later concepts. Do not reach for CTEs, window functions, lateral joins, or views in this phase. The point is to learn the basic row-set mechanics directly.

## Explain It Back

Explain the table grain, the join path, and the final output grain. Then explain one plausible wrong query and why it fails. A strong answer says, "I used this key because it represents the relationship," or, "I used a left join because the report must keep parents that have no child rows." It also says what would change if the business question changed.

## References and Further Reading

- PostgreSQL documentation for `SELECT`, joins, and aggregate functions is the syntax reference for these examples.
- `docs/glossary.md` defines foreign key and related curriculum vocabulary.

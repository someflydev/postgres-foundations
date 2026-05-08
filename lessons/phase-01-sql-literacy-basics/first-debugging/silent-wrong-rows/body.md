# Silent Wrong Rows

## Problem Framing

Phase 1 SQL starts with one table at a time. The learner is not trying to model the whole application, optimize a workload, or combine related tables. The immediate job is to look at a small table, name its columns, predict its rows, and then write a statement whose output can be checked by sight. In this lesson the working table is `scheduling.appointments` from the `scheduling` phase-1 seed pack. That table is intentionally small, so every mistake can be discussed as a concrete row rather than as an abstract rule. The habit is simple: inspect the shape, state the question in ordinary language, write the smallest SQL statement that answers it, and compare the output with the question.

## Minimal Concept Introduction

A table is a named collection of rows with the same column shape. A row is one recorded fact at the table's grain. A column is one named value available for each row. Phase 1 SQL uses `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `INSERT`, `UPDATE`, and `DELETE` without joins, grouping, subqueries, transactions, indexes, functions, JSON, or arrays. The important discipline is to keep the row set visible. If a predicate says `status = 'scheduled'`, point to the rows where that is true. If an order says descending, explain which value appears first. If a change statement has a `WHERE`, say which rows it protects from being changed.

## Worked Example

Run the seed first with `uv run pgfound content seed scheduling --phase 1 --reset`, then open `psql` with `make lab-psql`. A small worked example for this lesson is:

```sql
SELECT starts_at, status FROM scheduling.appointments WHERE starts_at BETWEEN '2026-02-10 00:00:00+00' AND '2026-02-10 23:59:59+00' ORDER BY starts_at;
```

Sample output from the phase-1 seed is:

```text
       starts_at        |  status
------------------------+-----------
 2026-02-11 17:00:00+00 | scheduled
(1 row)
```

The exact values come from the phase-1 seed pack. The useful check is not memorizing the output; it is proving that every returned row matches the selected columns, the filter if present, and the requested order.

## Diagnostic Questions

Before running a statement, ask what table supplies the rows. Then ask which columns are visible in the output and whether any expression changes a displayed value. If there is a `WHERE` clause, read it slowly as a row test. For `AND`, every part must be true. For `OR`, one part can be true. Parentheses matter because they make mixed `AND` and `OR` logic readable. For `IS NULL`, remember that it asks about missingness directly; equality to `NULL` is not the same idea. For ordering, ask whether ties need another column so the output is stable.

## Common Pitfalls

The first pitfall is reading a successful query as a correct query. PostgreSQL can return rows for the wrong question when the column name is valid and the predicate is too broad or too narrow. The second pitfall is trusting default row order. Without `ORDER BY`, a table has no teaching-order promise. The third pitfall is changing rows before selecting the exact rows that should change. For `UPDATE` and `DELETE`, first write the matching `SELECT`, confirm the row set, then use the same predicate in the change statement. The fourth pitfall is using later-course tools too early; joins and aggregates would hide the one-table reasoning this phase is building.

## Explain It Back

A good explanation names the table, the intended rows, and the columns returned or changed. For a read query, say: this statement reads `scheduling.appointments`, keeps rows that meet the predicate, sorts them by the named column, and returns only the selected columns. For a change query, say: this statement changes only rows matching the `WHERE` clause, and `RETURNING` shows the affected rows so the result is auditable. If the explanation cannot point to concrete rows in the seed data, the SQL is probably ahead of the reasoning.

## References and Further Reading

Use the local curriculum map for the Phase 1 boundary and the official PostgreSQL documentation when you need exact syntax. Keep the reading narrow: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and psql table inspection are enough here. Save joins, grouping, indexes, transactions, and advanced PostgreSQL data types for later phases, where the curriculum gives them the operational context they need.

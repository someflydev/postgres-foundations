# Solution

The two queries are not equivalent if the rewrite changes a presence test into a value-list test that can contain NULL. A common broken form is:

```sql
SELECT c.id
FROM ecommerce.customers c
WHERE c.id NOT IN (
    SELECT s.customer_id
    FROM ecommerce.customer_segments s
    WHERE s.segment <> 'wholesale'
);
```

If the subquery can produce NULL, `NOT IN` no longer means "no matching row";
the comparison becomes UNKNOWN for affected rows and can suppress results. A
CTE version that filters NULLs, or an `EXISTS` / `NOT EXISTS` version that keeps
the correlation explicit, has different semantics.

The preferred repair is to state the intended grain, then write the predicate as
presence or absence:

```sql
SELECT c.id, c.email
FROM ecommerce.customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM ecommerce.customer_segments s
    WHERE s.customer_id = c.id
      AND s.segment = 'wholesale'
)
ORDER BY c.email;
```

The diagnosis should say that the CTE itself was not the problem. The bug was
claiming equivalence while changing NULL-sensitive logic.

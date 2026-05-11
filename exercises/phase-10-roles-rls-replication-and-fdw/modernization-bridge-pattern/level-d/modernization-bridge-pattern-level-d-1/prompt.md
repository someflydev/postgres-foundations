# Modernization Bridge Pattern Level D1

## Setup

Use the Phase 10 modernization bridge corpus.

## Task

Diagnose an FDW query that joins local mapping rows to a foreign legacy account
table but is slow because the predicate is not pushed down. The problematic
shape wraps the foreign key in an expression:

```sql
SELECT *
FROM legacy.customer_mappings m
JOIN legacy_fdw.crm_accounts_1998 f
  ON lower(f.cust_no) = lower(m.external_customer_ref)
WHERE lower(f.cust_no) = 'c-100';
```

Rewrite the query so the foreign predicate can be pushed down more directly.

## Success Criteria

- Uses `EXPLAIN VERBOSE` or equivalent reasoning to identify pushdown risk.
- Avoids wrapping the foreign key column in the filter predicate.
- Explains why FDW latency makes pushdown matter.

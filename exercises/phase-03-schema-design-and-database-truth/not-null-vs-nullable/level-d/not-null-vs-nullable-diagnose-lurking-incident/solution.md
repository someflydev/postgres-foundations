# Solution

The missing invariant is that email and name are required customer facts, while phone may be a legitimate unknown. Without this constraint, an incident could occur when a customer row with NULL email cannot receive receipts and later joins silently drop it from contact workflows.

A concrete repair is:

```sql
UPDATE ecommerce.customers
SET created_at = now()
WHERE created_at IS NULL;

ALTER TABLE ecommerce.customers
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN created_at SET DEFAULT now(),
    ALTER COLUMN created_at SET NOT NULL;
```

Do not make every column NOT NULL by reflex. The repair should distinguish required facts from valid missingness and explain how that choice affects filters and aggregates.

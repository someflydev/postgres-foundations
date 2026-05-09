# Solution

The missing invariant is a deliberate split between row identity and business identity. Without this constraint, an incident could occur when a SKU changes or duplicates and downstream order_items either lose their stable target row or point at the wrong product.

A concrete repair is:

```sql
ALTER TABLE ecommerce.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);

ALTER TABLE ecommerce.products
    ALTER COLUMN sku SET NOT NULL;

ALTER TABLE ecommerce.products
    ADD CONSTRAINT products_sku_unique UNIQUE (sku);
```

Use `bigint generated always as identity` for the surrogate key in this phase. Keep the SKU as a natural business identifier enforced by UNIQUE, not as the only row identity unless the business has proved it never changes.

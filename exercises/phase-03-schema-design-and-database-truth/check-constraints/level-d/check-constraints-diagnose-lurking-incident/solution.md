# Solution

The missing invariant is that a line quantity must be positive and an appointment must start before it ends. Without this constraint, an incident could occur when refund processing inserts a negative quantity and inventory or revenue reports move in the wrong direction.

A concrete repair is:

```sql
ALTER TABLE ecommerce.order_items
    ALTER COLUMN quantity SET NOT NULL;

ALTER TABLE ecommerce.order_items
    ADD CONSTRAINT order_items_quantity_positive CHECK (quantity > 0);

ALTER TABLE scheduling.appointments
    ADD CONSTRAINT appointments_starts_before_ends CHECK (starts_at < ends_at);
```

These checks are row-local declarations. They do not need application code to remember the rule on every write path.

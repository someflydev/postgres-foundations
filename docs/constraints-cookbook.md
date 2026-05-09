# Constraints Cookbook

Phase 3 uses PostgreSQL constraints as executable design rules. Name the
business invariant first, then choose the smallest core constraint that enforces
it.

## UNIQUE

Use `UNIQUE` when a business identifier must not repeat.

```sql
ALTER TABLE ecommerce.customers
    ADD CONSTRAINT customers_email_unique UNIQUE (email);
```

Composite uniqueness protects a combination:

```sql
ALTER TABLE scheduling.appointments
    ADD CONSTRAINT appointments_provider_starts_at_unique
    UNIQUE (provider_id, starts_at);
```

PostgreSQL creates an automatic index for primary-key and unique constraints.
Phase 3 treats that as a correctness side effect, not as performance-tuning
material.

## CHECK

Use `CHECK` for row-local invariants.

```sql
ALTER TABLE ecommerce.order_items
    ADD CONSTRAINT order_items_quantity_positive CHECK (quantity > 0);

ALTER TABLE scheduling.appointments
    ADD CONSTRAINT appointments_starts_before_ends CHECK (starts_at < ends_at);
```

## NOT NULL

Use `NOT NULL` when the fact is required for every row. For existing tables,
clean or backfill first.

```sql
UPDATE ecommerce.customers
SET country_code = 'US'
WHERE country_code IS NULL;

ALTER TABLE ecommerce.customers
    ALTER COLUMN country_code SET NOT NULL;
```

## FOREIGN KEY

Use `FOREIGN KEY` to make a relationship enforceable.

```sql
ALTER TABLE ecommerce.orders
    ADD CONSTRAINT orders_customer_id_fkey
    FOREIGN KEY (customer_id) REFERENCES ecommerce.customers(id);
```

`ON DELETE` and `ON UPDATE` make the consequence explicit:

```sql
ALTER TABLE ecommerce.order_items
    ADD CONSTRAINT order_items_order_id_fkey
    FOREIGN KEY (order_id) REFERENCES ecommerce.orders(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;
```

Use cascading actions only when the business rule really says child rows should
follow parent changes or deletions.

## Reference Tables

Prefer a small table plus a foreign key when values need labels, metadata, or
future lifecycle rules.

```sql
CREATE TABLE scheduling.appointment_statuses (
    code text PRIMARY KEY,
    label text NOT NULL UNIQUE,
    is_terminal boolean NOT NULL DEFAULT false
);
```

## Generated Columns

Identity columns are the primary generated value in early phases:

```sql
id bigint generated always as identity PRIMARY KEY
```

Stored generated columns can derive a value from other columns:

```sql
line_total numeric(12,2)
    GENERATED ALWAYS AS (quantity * unit_price) STORED
```

Use them when the derived value is truly part of the schema contract.

## Future Pointer

Deferrable constraints are useful when a multi-step change needs constraints
checked later than each statement. Phase 3 mentions them only as a future topic;
transaction behavior is studied later.

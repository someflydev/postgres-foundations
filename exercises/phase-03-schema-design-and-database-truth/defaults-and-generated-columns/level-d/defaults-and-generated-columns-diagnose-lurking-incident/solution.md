# Solution

The missing invariant is that routine values should be generated consistently by PostgreSQL rather than improvised by every writer. Without this constraint, an incident could occur when one import omits created_at or computes a line total differently from the checkout service.

A concrete repair is:

```sql
CREATE TABLE ecommerce.order_line_drafts (
    id bigint generated always as identity PRIMARY KEY,
    quantity integer NOT NULL DEFAULT 1,
    unit_price numeric(12,2) NOT NULL DEFAULT 0,
    line_total numeric(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT order_line_drafts_quantity_positive CHECK (quantity > 0)
);
```

Keep defaults boring and truthful. A default should represent a safe assumption, not hide missing business input.

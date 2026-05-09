# Solution

The missing invariants are duplicate order numbers, nonpositive quantities, uncontrolled statuses, and impossible time ranges. Without this constraint, an incident could occur when a duplicate order number causes fulfillment to ship the wrong package or a negative quantity causes stock to increase during a sale.

A concrete repair is:

```sql
ALTER TABLE ecommerce.orders
    ADD CONSTRAINT orders_order_number_unique UNIQUE (order_number),
    ADD CONSTRAINT orders_total_amount_nonnegative CHECK (total_amount >= 0);

ALTER TABLE ecommerce.order_items
    ADD CONSTRAINT order_items_quantity_positive CHECK (quantity > 0);
```

A good review states the incident for each rule, then keeps the ALTER TABLE statements scoped to the missing invariants.

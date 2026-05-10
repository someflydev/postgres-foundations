# Solution

The running-total query is wrong when it relies on PostgreSQL's default frame:

```sql
sum(total_amount) OVER (
    PARTITION BY customer_id
    ORDER BY placed_at
)
```

With an `ORDER BY`, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND
CURRENT ROW`. Rows that tie on `placed_at` are peers, so the running total can
jump by multiple orders at once. That is a poor fit when the report is meant to
advance one physical order row at a time.

The repair is to make row-wise movement and tie ordering explicit:

```sql
SELECT
    customer_id,
    order_number,
    placed_at,
    total_amount,
    sum(total_amount) OVER (
        PARTITION BY customer_id
        ORDER BY placed_at, id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_customer_revenue
FROM ecommerce.orders
ORDER BY customer_id, placed_at, id;
```

The oral defense should call out both pieces: `ROWS` fixes peer grouping, and
`id` makes tied timestamps deterministic.

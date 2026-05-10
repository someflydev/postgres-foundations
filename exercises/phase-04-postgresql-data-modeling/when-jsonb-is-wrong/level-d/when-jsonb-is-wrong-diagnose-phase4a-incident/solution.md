# Reference Solution

The incident is an hourly report filtering `orders.metadata ->> 'channel'`; this could violate reporting correctness because typos and missing keys silently disappear. Migrate by adding `channel text`, backfilling from `metadata ->> 'channel'`, reviewing NULL and misspelled rows, adding a `CHECK` or reference table if the values are controlled, then changing writers to populate the column. The rewritten query is:

```sql
SELECT order_number
FROM ecommerce.orders
WHERE channel = 'web'
ORDER BY order_number;
```

Keep cold, rarely filtered details in JSONB. The bad-fit example is using JSONB for a hot predicate; the good-fit example is JSONB for sparse fulfillment metadata.

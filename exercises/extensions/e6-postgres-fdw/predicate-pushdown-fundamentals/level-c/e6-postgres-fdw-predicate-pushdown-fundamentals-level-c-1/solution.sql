EXPLAIN (VERBOSE, COSTS OFF)
SELECT external_order_ref, external_customer_ref, order_total
FROM legacy_fdw.legacy_orders
WHERE currency = 'USD'
  AND order_total >= 100;
-- Critical drill: configure predicate pushdown to a foreign table and demonstrate EXPLAIN VERBOSE showing the pushdown.

EXPLAIN (VERBOSE, COSTS OFF)
SELECT external_order_ref, external_customer_ref, order_total
FROM legacy_fdw.legacy_orders
WHERE currency = 'USD'
ORDER BY external_order_ref
LIMIT 20;

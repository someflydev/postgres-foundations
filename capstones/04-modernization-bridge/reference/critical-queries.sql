REFRESH MATERIALIZED VIEW new_service.legacy_customer_order_totals;

SELECT l.local_customer_ref, l.legacy_customer_id
FROM new_service.customer_links l
WHERE l.tenant_id = '00000000-0000-0000-0000-000000000401'::uuid
  AND l.local_customer_ref = 'CUST-100';

SELECT l.local_customer_ref, t.order_count, t.lifetime_total, t.last_ordered_at
FROM new_service.customer_links l
JOIN new_service.legacy_customer_order_totals t
  ON t.legacy_customer_id = l.legacy_customer_id
WHERE l.tenant_id = '00000000-0000-0000-0000-000000000401'::uuid
ORDER BY t.lifetime_total DESC
LIMIT 20;

SELECT id, order_status, created_at
FROM new_service.local_orders
WHERE tenant_id = '00000000-0000-0000-0000-000000000401'::uuid
ORDER BY created_at DESC
LIMIT 50;

SELECT l.legacy_customer_id
FROM new_service.customer_links l
LEFT JOIN new_service.legacy_customer_order_totals t
  ON t.legacy_customer_id = l.legacy_customer_id
WHERE l.tenant_id = '00000000-0000-0000-0000-000000000401'::uuid
  AND t.legacy_customer_id IS NULL;

SELECT c.legacy_customer_id, c.customer_name, c.status
FROM new_service.customer_links l
JOIN legacy_fdw.customers c
  ON c.legacy_customer_id = l.legacy_customer_id
WHERE l.tenant_id = '00000000-0000-0000-0000-000000000401'::uuid
  AND l.local_customer_ref = 'CUST-100';

SELECT o.legacy_order_id, o.ordered_at, o.status, o.order_total
FROM new_service.customer_links l
JOIN legacy_fdw.orders o
  ON o.legacy_customer_id = l.legacy_customer_id
WHERE l.tenant_id = '00000000-0000-0000-0000-000000000401'::uuid
  AND l.local_customer_ref = 'CUST-100'
ORDER BY o.ordered_at DESC
LIMIT 25;

SELECT p.legacy_product_id, p.sku, p.product_name
FROM legacy_fdw.products p
WHERE p.active IS TRUE
ORDER BY p.sku
LIMIT 50;

SELECT c.legacy_customer_id, c.customer_name
FROM legacy_fdw.customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM new_service.customer_links l
    WHERE l.legacy_customer_id = c.legacy_customer_id
)
ORDER BY c.legacy_customer_id
LIMIT 50;

EXPLAIN (VERBOSE, COSTS OFF)
SELECT c.legacy_customer_id, c.customer_name
FROM legacy_fdw.customers c
WHERE c.legacy_customer_id = 100;

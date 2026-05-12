-- One acceptable answer for e7-citus-citus-on-managed-services-level-c-1.
-- Use Citus evidence for managed Citus posture, with Azure Cosmos DB for PostgreSQL as the primary managed story. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE EXTENSION IF NOT EXISTS citus;
SELECT create_reference_table('customers');
SELECT create_reference_table('products');
DROP TABLE IF EXISTS citus_order_items_by_customer;
DROP TABLE IF EXISTS citus_orders;
CREATE TABLE citus_orders AS
SELECT id AS order_id, customer_id, order_number, status, total_amount, placed_at
FROM orders;
CREATE TABLE citus_order_items_by_customer AS
SELECT oi.id AS order_item_id, oi.order_id, o.customer_id, oi.product_id, oi.quantity, oi.unit_price
FROM order_items AS oi
JOIN orders AS o ON o.id = oi.order_id;
SELECT create_distributed_table('citus_orders', 'customer_id');
SELECT create_distributed_table('citus_order_items_by_customer', 'customer_id', colocate_with => 'citus_orders');
EXPLAIN SELECT o.order_number, sum(oi.quantity * oi.unit_price) AS item_revenue
FROM citus_orders AS o
JOIN citus_order_items_by_customer AS oi
  ON oi.customer_id = o.customer_id
 AND oi.order_id = o.order_id
WHERE o.customer_id = 42
GROUP BY o.order_number;

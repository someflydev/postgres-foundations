DROP INDEX IF EXISTS ecommerce.customers_lower_email_idx;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email, full_name
FROM ecommerce.customers
WHERE lower(email) = lower('PHASE7A-CUSTOMER-00042@EXAMPLE.COM');
CREATE INDEX customers_lower_email_idx
ON ecommerce.customers (lower(email));
ANALYZE ecommerce.customers;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email, full_name
FROM ecommerce.customers
WHERE lower(email) = lower('PHASE7A-CUSTOMER-00042@EXAMPLE.COM');

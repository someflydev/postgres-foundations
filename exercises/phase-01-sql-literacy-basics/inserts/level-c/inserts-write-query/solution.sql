INSERT INTO ecommerce.products (sku, name, price, currency, stock_on_hand) VALUES ('TEE-PG-001', 'Postgres T-Shirt', 24.00, 'USD', 12) RETURNING sku, name, currency;

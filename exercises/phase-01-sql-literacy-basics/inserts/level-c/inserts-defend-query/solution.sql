INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES ('PATCH-PG-001', 'Postgres Patch', 6.00, 60), ('LANYARD-PG-001', 'Postgres Lanyard', 7.50, 45) RETURNING sku, name;

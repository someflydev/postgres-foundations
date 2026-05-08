INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES ('PIN-PG-001', 'Postgres Pin', 4.00, 80), ('NOTE-PG-001', 'Postgres Notebook', 9.00, 35) RETURNING sku, stock_on_hand;

INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES ('BAG-PG-001', 'Postgres Tote', 18.00, 20) RETURNING sku, name, stock_on_hand;

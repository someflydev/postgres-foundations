INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES ('CARD-PG-001', 'Postgres Sticker Pack', 5.00, 100) RETURNING sku, name, price;

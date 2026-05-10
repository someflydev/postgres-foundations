-- domain: ecommerce
-- phase: 05
-- depends: phase-04b
-- expected rows: >= 220 customers, >= 2400 orders, >= 2400 generated order_items, 9 categories
-- description: expressive-querying volume for CTEs, windows, lateral joins, upserts, views, and matviews

CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.categories (
    id bigint generated always as identity PRIMARY KEY,
    parent_id bigint REFERENCES ecommerce.categories(id),
    name text NOT NULL UNIQUE
);

INSERT INTO ecommerce.categories (name, parent_id)
VALUES
    ('Catalog', NULL),
    ('Books', (SELECT id FROM ecommerce.categories WHERE name = 'Catalog')),
    ('Merch', (SELECT id FROM ecommerce.categories WHERE name = 'Catalog')),
    ('Training', (SELECT id FROM ecommerce.categories WHERE name = 'Books')),
    ('Reference', (SELECT id FROM ecommerce.categories WHERE name = 'Books')),
    ('Apparel', (SELECT id FROM ecommerce.categories WHERE name = 'Merch')),
    ('Desk', (SELECT id FROM ecommerce.categories WHERE name = 'Merch')),
    ('Stickers', (SELECT id FROM ecommerce.categories WHERE name = 'Desk')),
    ('Mugs', (SELECT id FROM ecommerce.categories WHERE name = 'Desk'))
ON CONFLICT (name) DO UPDATE SET parent_id = EXCLUDED.parent_id;

INSERT INTO ecommerce.customers (email, full_name, created_at)
SELECT format('phase5-customer-%s@example.com', gs), format('Phase Five Customer %s', gs),
       '2025-05-01 00:00:00+00'::timestamptz + (gs || ' days')::interval
FROM generate_series(1, 220) AS gs
ON CONFLICT (email) DO NOTHING;

INSERT INTO ecommerce.products (sku, name, price, currency, stock_on_hand, tags)
SELECT format('P5-SKU-%s', gs), format('Phase Five Product %s', gs),
       (8 + (gs % 17) * 3)::numeric(12,2), 'USD', 100 + gs,
       ARRAY['phase5', CASE WHEN gs % 2 = 0 THEN 'recurring' ELSE 'seasonal' END]
FROM generate_series(1, 18) AS gs
ON CONFLICT (sku) DO NOTHING;

WITH numbered_customers AS (
    SELECT id, row_number() OVER (ORDER BY email) AS rn
    FROM ecommerce.customers
    WHERE email LIKE 'phase5-customer-%@example.com'
), generated_orders AS (
    SELECT gs AS n,
           ((gs - 1) % 220) + 1 AS customer_rn,
           'P5-ORD-' || lpad(gs::text, 5, '0') AS order_number,
           '2025-06-01 00:00:00+00'::timestamptz + ((gs - 1) % 365) * interval '1 day' + ((gs % 8) * interval '1 hour') AS placed_at,
           (25 + (gs % 11) * 9 + (gs % 5) * 1.75)::numeric(12,2) AS total_amount,
           CASE WHEN gs % 13 = 0 THEN 'cancelled' WHEN gs % 5 = 0 THEN 'shipped' ELSE 'paid' END AS status
    FROM generate_series(1, 2400) AS gs
)
INSERT INTO ecommerce.orders (customer_id, order_number, status, total_amount, currency, placed_at)
SELECT c.id, g.order_number, g.status, g.total_amount, 'USD', g.placed_at
FROM generated_orders g
JOIN numbered_customers c ON c.rn = g.customer_rn
ON CONFLICT (order_number) DO NOTHING;

WITH generated_orders AS (
    SELECT id, order_number, total_amount, row_number() OVER (ORDER BY order_number) AS rn
    FROM ecommerce.orders
    WHERE order_number LIKE 'P5-ORD-%'
), numbered_products AS (
    SELECT id, row_number() OVER (ORDER BY sku) AS rn
    FROM ecommerce.products
    WHERE sku LIKE 'P5-SKU-%'
)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price, currency)
SELECT o.id, p.id, 1 + (o.rn % 3), round((o.total_amount / (1 + (o.rn % 3)))::numeric, 2), 'USD'
FROM generated_orders o
JOIN numbered_products p ON p.rn = ((o.rn - 1) % 18) + 1
WHERE NOT EXISTS (
    SELECT 1 FROM ecommerce.order_items existing
    WHERE existing.order_id = o.id AND existing.product_id = p.id
);

CREATE TABLE IF NOT EXISTS ecommerce.customer_segments (
    customer_id bigint PRIMARY KEY REFERENCES ecommerce.customers(id),
    segment text
);

INSERT INTO ecommerce.customer_segments (customer_id, segment)
SELECT id,
       CASE WHEN row_number() OVER (ORDER BY email) % 17 = 0 THEN NULL
            WHEN row_number() OVER (ORDER BY email) % 5 = 0 THEN 'wholesale'
            ELSE 'retail' END
FROM ecommerce.customers
WHERE email LIKE 'phase5-customer-%@example.com'
ON CONFLICT (customer_id) DO UPDATE SET segment = EXCLUDED.segment;

CREATE TABLE IF NOT EXISTS ecommerce.product_daily_inventory (
    sku text NOT NULL REFERENCES ecommerce.products(sku),
    snapshot_date date NOT NULL,
    quantity_on_hand integer NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (sku, snapshot_date)
);

INSERT INTO ecommerce.product_daily_inventory (sku, snapshot_date, quantity_on_hand)
SELECT sku, DATE '2026-05-01', stock_on_hand
FROM ecommerce.products
WHERE sku LIKE 'P5-SKU-%' OR sku IN ('BK-SQL-001', 'MUG-PG-001')
ON CONFLICT (sku, snapshot_date) DO UPDATE
SET quantity_on_hand = EXCLUDED.quantity_on_hand,
    updated_at = now();

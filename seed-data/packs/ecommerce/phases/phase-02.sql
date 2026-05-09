-- domain: ecommerce
-- phase: 02
-- depends: phase-01
-- description: line items for joins and aggregate grain

CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.order_items (
    id bigint generated always as identity PRIMARY KEY,
    order_id bigint NOT NULL REFERENCES ecommerce.orders(id),
    product_id bigint NOT NULL REFERENCES ecommerce.products(id),
    quantity integer NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    currency text NOT NULL DEFAULT 'USD',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO ecommerce.customers (email, full_name)
VALUES
    ('lin@example.com', 'Lin Moreno'),
    ('no-orders@example.com', 'No Orders')
ON CONFLICT (email) DO NOTHING;

INSERT INTO ecommerce.products (sku, name, price, currency, stock_on_hand)
VALUES
    ('STK-PG-001', 'Postgres Sticker Pack', 5.00, 'USD', 200),
    ('CAP-PG-001', 'Postgres Cap', 22.00, 'USD', 15)
ON CONFLICT (sku) DO NOTHING;

INSERT INTO ecommerce.orders (customer_id, order_number, status, total_amount, currency, placed_at)
VALUES
    (
        (SELECT id FROM ecommerce.customers WHERE email = 'lin@example.com'),
        'EC-1003',
        'paid',
        27.00,
        'USD',
        '2026-01-07 18:00:00+00'
    )
ON CONFLICT (order_number) DO NOTHING;

INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price, currency)
SELECT o.id, p.id, item.quantity, item.unit_price, 'USD'
FROM (
    VALUES
        ('EC-1001', 'BK-SQL-001', 1, 29.00),
        ('EC-1001', 'MUG-PG-001', 1, 14.50),
        ('EC-1002', 'BK-SQL-001', 1, 29.00),
        ('EC-1003', 'STK-PG-001', 1, 5.00),
        ('EC-1003', 'CAP-PG-001', 1, 22.00)
) AS item(order_number, sku, quantity, unit_price)
INNER JOIN ecommerce.orders o ON o.order_number = item.order_number
INNER JOIN ecommerce.products p ON p.sku = item.sku
WHERE NOT EXISTS (
    SELECT 1
    FROM ecommerce.order_items existing
    WHERE existing.order_id = o.id
      AND existing.product_id = p.id
      AND existing.quantity = item.quantity
      AND existing.unit_price = item.unit_price
);

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
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (order_id, product_id)
);

INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price, currency)
VALUES
    (
        (SELECT id FROM ecommerce.orders WHERE order_number = 'EC-1001'),
        (SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'),
        1,
        29.00,
        'USD'
    ),
    (
        (SELECT id FROM ecommerce.orders WHERE order_number = 'EC-1001'),
        (SELECT id FROM ecommerce.products WHERE sku = 'MUG-PG-001'),
        1,
        14.50,
        'USD'
    ),
    (
        (SELECT id FROM ecommerce.orders WHERE order_number = 'EC-1002'),
        (SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'),
        1,
        29.00,
        'USD'
    )
ON CONFLICT (order_id, product_id) DO NOTHING;

-- domain: ecommerce
-- phase: 04b
-- depends: phase-04a
-- description: array tags and price-history contrast for PostgreSQL type modeling

CREATE SCHEMA IF NOT EXISTS ecommerce;

ALTER TABLE ecommerce.products
    ADD COLUMN IF NOT EXISTS tags text[] NOT NULL DEFAULT '{}'::text[];

UPDATE ecommerce.products
SET tags = CASE sku
    WHEN 'BK-SQL-001' THEN ARRAY['book', 'postgres', 'training']
    WHEN 'MUG-PG-001' THEN ARRAY['merch', 'postgres', 'gift']
    ELSE ARRAY['catalog']
END
WHERE tags = '{}'::text[];

CREATE TABLE IF NOT EXISTS ecommerce.price_history (
    id bigint generated always as identity PRIMARY KEY,
    product_id bigint NOT NULL REFERENCES ecommerce.products(id),
    valid_from timestamptz NOT NULL,
    valid_until timestamptz,
    price numeric(12,2) NOT NULL,
    currency text NOT NULL DEFAULT 'USD',
    recorded_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (product_id, valid_from),
    CONSTRAINT price_history_price_nonnegative CHECK (price >= 0),
    CONSTRAINT price_history_time_order_check
        CHECK (valid_until IS NULL OR valid_from < valid_until)
);

INSERT INTO ecommerce.price_history (product_id, valid_from, valid_until, price, currency)
VALUES
    (
        (SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'),
        '2026-01-01 00:00:00+00',
        '2026-03-01 00:00:00+00',
        24.00,
        'USD'
    ),
    (
        (SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'),
        '2026-03-01 00:00:00+00',
        NULL,
        29.00,
        'USD'
    ),
    (
        (SELECT id FROM ecommerce.products WHERE sku = 'MUG-PG-001'),
        '2026-01-01 00:00:00+00',
        NULL,
        14.50,
        'USD'
    )
ON CONFLICT DO NOTHING;

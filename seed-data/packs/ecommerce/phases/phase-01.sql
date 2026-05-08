-- domain: ecommerce
-- phase: 01
-- depends: none
-- description: minimal schema + small seed

CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.customers (
    id bigint generated always as identity PRIMARY KEY,
    email text NOT NULL UNIQUE,
    full_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ecommerce.products (
    id bigint generated always as identity PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    name text NOT NULL,
    price numeric(12,2) NOT NULL,
    currency text NOT NULL DEFAULT 'USD',
    stock_on_hand integer NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ecommerce.orders (
    id bigint generated always as identity PRIMARY KEY,
    customer_id bigint NOT NULL REFERENCES ecommerce.customers(id),
    order_number text NOT NULL UNIQUE,
    status text NOT NULL DEFAULT 'placed',
    total_amount numeric(12,2) NOT NULL,
    currency text NOT NULL DEFAULT 'USD',
    placed_at timestamptz NOT NULL DEFAULT now(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO ecommerce.customers (email, full_name)
OVERRIDING SYSTEM VALUE
VALUES
    ('ada@example.com', 'Ada Lovelace'),
    ('grace@example.com', 'Grace Hopper')
ON CONFLICT (email) DO NOTHING;

INSERT INTO ecommerce.products (sku, name, price, currency, stock_on_hand)
OVERRIDING SYSTEM VALUE
VALUES
    ('BK-SQL-001', 'SQL Field Guide', 29.00, 'USD', 25),
    ('MUG-PG-001', 'Postgres Mug', 14.50, 'USD', 40)
ON CONFLICT (sku) DO NOTHING;

INSERT INTO ecommerce.orders (customer_id, order_number, status, total_amount, currency, placed_at)
VALUES
    ((SELECT id FROM ecommerce.customers WHERE email = 'ada@example.com'), 'EC-1001', 'placed', 43.50, 'USD', '2026-01-05 15:00:00+00'),
    ((SELECT id FROM ecommerce.customers WHERE email = 'grace@example.com'), 'EC-1002', 'paid', 29.00, 'USD', '2026-01-06 16:30:00+00')
ON CONFLICT (order_number) DO NOTHING;

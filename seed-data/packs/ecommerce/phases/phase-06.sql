-- domain: ecommerce
-- phase: 06
-- depends: phase-05
-- expected rows: hot inventory rows and reservation rows for concurrency drills
-- description: transaction, isolation, lost-update, idempotency, and deadlock practice

CREATE SCHEMA IF NOT EXISTS ecommerce;
CREATE SCHEMA IF NOT EXISTS bank;

CREATE TABLE IF NOT EXISTS ecommerce.inventory (
    product_id bigint PRIMARY KEY REFERENCES ecommerce.products(id),
    quantity_on_hand integer NOT NULL CHECK (quantity_on_hand >= 0),
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO ecommerce.inventory (product_id, quantity_on_hand)
SELECT id,
       CASE sku
           WHEN 'BK-SQL-001' THEN 1
           WHEN 'MUG-PG-001' THEN 2
           ELSE 15
       END
FROM ecommerce.products
WHERE sku IN ('BK-SQL-001', 'MUG-PG-001', 'P5-SKU-1', 'P5-SKU-2')
ON CONFLICT (product_id) DO UPDATE
SET quantity_on_hand = EXCLUDED.quantity_on_hand,
    updated_at = now();

CREATE TABLE IF NOT EXISTS ecommerce.order_reservations (
    id bigint generated always as identity PRIMARY KEY,
    order_id bigint NOT NULL REFERENCES ecommerce.orders(id),
    product_id bigint NOT NULL REFERENCES ecommerce.products(id),
    quantity integer NOT NULL CHECK (quantity > 0),
    idempotency_key text UNIQUE,
    reserved_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO ecommerce.order_reservations (order_id, product_id, quantity, idempotency_key, reserved_at)
SELECT o.id, p.id, 1, 'phase6-existing-reservation', '2026-05-10 09:00:00+00'
FROM ecommerce.orders o
CROSS JOIN ecommerce.products p
WHERE o.order_number = 'EC-1001'
  AND p.sku = 'BK-SQL-001'
ON CONFLICT (idempotency_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS bank.accounts (
    id bigint generated always as identity PRIMARY KEY,
    account_number text NOT NULL UNIQUE,
    balance numeric(12,2) NOT NULL CHECK (balance >= 0),
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO bank.accounts (account_number, balance)
VALUES
    ('phase6-a', 100.00),
    ('phase6-b', 100.00)
ON CONFLICT (account_number) DO UPDATE
SET balance = EXCLUDED.balance,
    updated_at = now();

CREATE TABLE IF NOT EXISTS bank.funds_transfer (
    id bigint generated always as identity PRIMARY KEY,
    from_account bigint NOT NULL REFERENCES bank.accounts(id),
    to_account bigint NOT NULL REFERENCES bank.accounts(id),
    amount numeric(12,2) NOT NULL CHECK (amount > 0),
    requested_at timestamptz NOT NULL DEFAULT now()
);

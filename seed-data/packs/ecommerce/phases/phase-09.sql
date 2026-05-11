-- domain: ecommerce
-- phase: 09
-- depends: phase-08
-- expected rows: mirrors generated order history when phase 7a was loaded
-- description: quarterly range-partitioned order table for comparison with ecommerce.orders

CREATE SCHEMA IF NOT EXISTS ecommerce;

DROP TABLE IF EXISTS ecommerce.orders_partitioned CASCADE;

CREATE TABLE ecommerce.orders_partitioned (
    order_id bigint NOT NULL,
    customer_id bigint NOT NULL REFERENCES ecommerce.customers(id),
    order_number text NOT NULL,
    status text NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    currency text NOT NULL DEFAULT 'USD',
    ordered_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    PRIMARY KEY (order_id, ordered_at),
    UNIQUE (order_number, ordered_at)
) PARTITION BY RANGE (ordered_at);

CREATE TABLE ecommerce.orders_partitioned_2025_q1 PARTITION OF ecommerce.orders_partitioned
    FOR VALUES FROM ('2025-01-01 00:00:00+00') TO ('2025-04-01 00:00:00+00');
CREATE TABLE ecommerce.orders_partitioned_2025_q2 PARTITION OF ecommerce.orders_partitioned
    FOR VALUES FROM ('2025-04-01 00:00:00+00') TO ('2025-07-01 00:00:00+00');
CREATE TABLE ecommerce.orders_partitioned_2025_q3 PARTITION OF ecommerce.orders_partitioned
    FOR VALUES FROM ('2025-07-01 00:00:00+00') TO ('2025-10-01 00:00:00+00');
CREATE TABLE ecommerce.orders_partitioned_2025_q4 PARTITION OF ecommerce.orders_partitioned
    FOR VALUES FROM ('2025-10-01 00:00:00+00') TO ('2026-01-01 00:00:00+00');
CREATE TABLE ecommerce.orders_partitioned_2026_q1 PARTITION OF ecommerce.orders_partitioned
    FOR VALUES FROM ('2026-01-01 00:00:00+00') TO ('2026-04-01 00:00:00+00');
CREATE TABLE ecommerce.orders_partitioned_2026_q2 PARTITION OF ecommerce.orders_partitioned
    FOR VALUES FROM ('2026-04-01 00:00:00+00') TO ('2026-07-01 00:00:00+00');
CREATE TABLE ecommerce.orders_partitioned_default PARTITION OF ecommerce.orders_partitioned DEFAULT;

CREATE INDEX orders_partitioned_ordered_at_brin
ON ecommerce.orders_partitioned USING brin (ordered_at);

CREATE INDEX orders_partitioned_customer_ordered_at_idx
ON ecommerce.orders_partitioned (customer_id, ordered_at DESC);

CREATE INDEX orders_partitioned_status_ordered_at_idx
ON ecommerce.orders_partitioned (status, ordered_at DESC);

INSERT INTO ecommerce.orders_partitioned (
    order_id,
    customer_id,
    order_number,
    status,
    total_amount,
    currency,
    ordered_at,
    created_at,
    updated_at
)
SELECT
    id,
    customer_id,
    order_number,
    status,
    total_amount,
    currency,
    placed_at,
    created_at,
    updated_at
FROM ecommerce.orders
WHERE placed_at >= '2025-01-01 00:00:00+00'
  AND placed_at < '2026-07-01 00:00:00+00';

ANALYZE ecommerce.orders_partitioned;

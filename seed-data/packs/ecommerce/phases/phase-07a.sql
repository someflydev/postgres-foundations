-- domain: ecommerce
-- phase: 07a
-- depends: phase-06
-- expected rows: >= 200k orders, >= 1M order_items, >= 5k products after generated COPY load
-- description: large order history for scan, B-tree, and composite-index planning labs

CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE UNLOGGED TABLE IF NOT EXISTS ecommerce.phase_07a_products_stage (
    sku text PRIMARY KEY,
    name text NOT NULL,
    price numeric(12,2) NOT NULL,
    stock_on_hand integer NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE UNLOGGED TABLE IF NOT EXISTS ecommerce.phase_07a_customers_stage (
    email text PRIMARY KEY,
    full_name text NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE UNLOGGED TABLE IF NOT EXISTS ecommerce.phase_07a_orders_stage (
    customer_email text NOT NULL,
    order_number text PRIMARY KEY,
    status text NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    placed_at timestamptz NOT NULL
);

CREATE UNLOGGED TABLE IF NOT EXISTS ecommerce.phase_07a_order_items_stage (
    order_number text NOT NULL,
    sku text NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE INDEX IF NOT EXISTS phase_07a_order_items_stage_order_number_idx
ON ecommerce.phase_07a_order_items_stage (order_number);

CREATE INDEX IF NOT EXISTS phase_07a_order_items_stage_sku_idx
ON ecommerce.phase_07a_order_items_stage (sku);

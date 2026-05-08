-- domain: modernization_bridge
-- phase: 01
-- depends: none
-- description: minimal schema + small seed

CREATE SCHEMA IF NOT EXISTS legacy;

CREATE TABLE IF NOT EXISTS legacy.legacy_customers (
    id bigint generated always as identity PRIMARY KEY,
    source_system text NOT NULL,
    external_customer_ref text NOT NULL,
    display_name text NOT NULL,
    email text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_system, external_customer_ref)
);

CREATE TABLE IF NOT EXISTS legacy.legacy_orders (
    id bigint generated always as identity PRIMARY KEY,
    source_system text NOT NULL,
    external_order_ref text NOT NULL,
    external_customer_ref text NOT NULL,
    order_total numeric(12,2) NOT NULL,
    currency text NOT NULL DEFAULT 'USD',
    placed_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_system, external_order_ref)
);

INSERT INTO legacy.legacy_customers (source_system, external_customer_ref, display_name, email)
VALUES
    ('crm_v1', 'C-100', 'Old Co', 'ops@oldco.example'),
    ('crm_v1', 'C-101', 'River Shop', NULL)
ON CONFLICT (source_system, external_customer_ref) DO NOTHING;

INSERT INTO legacy.legacy_orders (source_system, external_order_ref, external_customer_ref, order_total, currency, placed_at)
VALUES
    ('crm_v1', 'O-900', 'C-100', 199.00, 'USD', '2025-12-15 14:30:00+00'),
    ('crm_v1', 'O-901', 'C-101', 49.95, 'USD', '2025-12-16 15:45:00+00')
ON CONFLICT (source_system, external_order_ref) DO NOTHING;

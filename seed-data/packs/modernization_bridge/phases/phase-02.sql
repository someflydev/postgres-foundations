-- domain: modernization_bridge
-- phase: 02
-- depends: phase-01
-- description: import batches and customer mappings for migration joins

CREATE SCHEMA IF NOT EXISTS legacy;

CREATE TABLE IF NOT EXISTS legacy.import_batches (
    id bigint generated always as identity PRIMARY KEY,
    source_system text NOT NULL,
    batch_key text NOT NULL UNIQUE,
    imported_at timestamptz NOT NULL,
    row_count integer NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS legacy.customer_mappings (
    id bigint generated always as identity PRIMARY KEY,
    source_system text NOT NULL,
    external_customer_ref text NOT NULL,
    canonical_customer_ref text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_system, external_customer_ref)
);

INSERT INTO legacy.import_batches (source_system, batch_key, imported_at, row_count)
VALUES
    ('crm_v1', 'crm-v1-2025-12-17', '2025-12-17 02:00:00+00', 4)
ON CONFLICT (batch_key) DO NOTHING;

INSERT INTO legacy.customer_mappings (source_system, external_customer_ref, canonical_customer_ref)
VALUES
    ('crm_v1', 'C-100', 'cust-old-co'),
    ('crm_v1', 'C-101', 'cust-river-shop')
ON CONFLICT (source_system, external_customer_ref) DO NOTHING;

CREATE SCHEMA legacy_fdw;
CREATE SCHEMA new_service;

CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER legacy_monolith
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'pg-replica', dbname 'pgfound', port '5432');

CREATE USER MAPPING IF NOT EXISTS FOR CURRENT_USER
    SERVER legacy_monolith
    OPTIONS (user 'pgfound', password 'pgfound');

CREATE FOREIGN TABLE legacy_fdw.customers (
    legacy_customer_id bigint NOT NULL,
    tenant_code text NOT NULL,
    customer_name text NOT NULL,
    status text NOT NULL,
    updated_at timestamptz NOT NULL
) SERVER legacy_monolith OPTIONS (schema_name 'legacy', table_name 'customers');

CREATE FOREIGN TABLE legacy_fdw.orders (
    legacy_order_id bigint NOT NULL,
    legacy_customer_id bigint NOT NULL,
    ordered_at timestamptz NOT NULL,
    status text NOT NULL,
    order_total numeric(12, 2) NOT NULL
) SERVER legacy_monolith OPTIONS (schema_name 'legacy', table_name 'orders');

CREATE FOREIGN TABLE legacy_fdw.products (
    legacy_product_id bigint NOT NULL,
    sku text NOT NULL,
    product_name text NOT NULL,
    active boolean NOT NULL
) SERVER legacy_monolith OPTIONS (schema_name 'legacy', table_name 'products');

CREATE TABLE new_service.tenants (
    id uuid PRIMARY KEY,
    tenant_code text NOT NULL UNIQUE,
    name text NOT NULL
);

CREATE TABLE new_service.customer_links (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES new_service.tenants(id),
    local_customer_ref text NOT NULL,
    legacy_customer_id bigint NOT NULL,
    linked_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, local_customer_ref),
    UNIQUE (tenant_id, legacy_customer_id)
);

CREATE TABLE new_service.local_orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES new_service.tenants(id),
    customer_link_id bigint NOT NULL REFERENCES new_service.customer_links(id),
    order_status text NOT NULL CHECK (order_status IN ('draft', 'submitted', 'cancelled')),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE MATERIALIZED VIEW new_service.legacy_customer_order_totals AS
SELECT
    c.legacy_customer_id,
    count(o.legacy_order_id) AS order_count,
    coalesce(sum(o.order_total), 0::numeric) AS lifetime_total,
    max(o.ordered_at) AS last_ordered_at
FROM legacy_fdw.customers c
LEFT JOIN legacy_fdw.orders o ON o.legacy_customer_id = c.legacy_customer_id
GROUP BY c.legacy_customer_id
WITH NO DATA;

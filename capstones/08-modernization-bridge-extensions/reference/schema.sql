CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SCHEMA IF NOT EXISTS bridge_ext;
CREATE SCHEMA IF NOT EXISTS legacy_fdw;

CREATE TABLE bridge_ext.accounts (
    account_id bigserial PRIMARY KEY,
    tenant_id text NOT NULL,
    legacy_customer_id bigint,
    account_name text NOT NULL,
    notes text NOT NULL DEFAULT '',
    search_tsv tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', account_name), 'A') ||
        setweight(to_tsvector('english', notes), 'B')
    ) STORED
);

CREATE TABLE bridge_ext.orders (
    order_id bigserial PRIMARY KEY,
    account_id bigint NOT NULL REFERENCES bridge_ext.accounts(account_id),
    order_total numeric(12,2) NOT NULL,
    booked_at timestamptz NOT NULL DEFAULT now()
);

CREATE MATERIALIZED VIEW bridge_ext.bi_account_order_totals AS
SELECT a.tenant_id, a.account_id, count(o.order_id) AS order_count, coalesce(sum(o.order_total), 0) AS total_value
FROM bridge_ext.accounts a
LEFT JOIN bridge_ext.orders o ON o.account_id = a.account_id
GROUP BY a.tenant_id, a.account_id
WITH NO DATA;

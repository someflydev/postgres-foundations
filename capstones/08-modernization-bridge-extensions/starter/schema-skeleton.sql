CREATE SCHEMA IF NOT EXISTS bridge_ext;

CREATE TABLE bridge_ext.accounts (
    account_id bigserial PRIMARY KEY,
    tenant_id text NOT NULL,
    account_name text NOT NULL
);

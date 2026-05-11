-- domain: modernization_bridge
-- phase: 10
-- depends: phase-02
-- description: loopback postgres_fdw bridge to legacy schema

CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE SCHEMA IF NOT EXISTS legacy;
CREATE SCHEMA IF NOT EXISTS legacy_fdw;

CREATE TABLE IF NOT EXISTS legacy.crm_accounts_1998 (
    cust_no text PRIMARY KEY,
    company text NOT NULL,
    contact_email text,
    last_invoice_total numeric(12,2) NOT NULL DEFAULT 0,
    active_flag char(1) NOT NULL DEFAULT 'Y',
    loaded_from_file text NOT NULL DEFAULT 'crm_accounts_1998.csv'
);

CREATE TABLE IF NOT EXISTS legacy.crm_notes_1998 (
    note_no bigint generated always as identity PRIMARY KEY,
    cust_no text NOT NULL,
    note_text text NOT NULL,
    entered_by text NOT NULL,
    entered_on date NOT NULL
);

INSERT INTO legacy.crm_accounts_1998 (
    cust_no,
    company,
    contact_email,
    last_invoice_total,
    active_flag
)
VALUES
    ('C-100', 'Old Co', 'ops@oldco.example', 199.00, 'Y'),
    ('C-101', 'River Shop', NULL, 49.95, 'Y'),
    ('C-404', 'Dormant File Only', NULL, 0.00, 'N')
ON CONFLICT (cust_no) DO NOTHING;

INSERT INTO legacy.crm_notes_1998 (cust_no, note_text, entered_by, entered_on)
VALUES
    ('C-100', 'Still bills through old CRM account number.', 'migrations', '2026-01-08'),
    ('C-101', 'Email missing in source; enrich before cutover.', 'migrations', '2026-01-09')
ON CONFLICT DO NOTHING;

DROP SERVER IF EXISTS legacy_loopback CASCADE;
CREATE SERVER legacy_loopback
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (
        host '127.0.0.1',
        port '5432',
        dbname 'pgfound'
    );

CREATE USER MAPPING FOR CURRENT_USER
    SERVER legacy_loopback
    OPTIONS (
        user 'pgfound',
        password 'pgfound'
    );

IMPORT FOREIGN SCHEMA legacy
    LIMIT TO (legacy_customers, legacy_orders)
    FROM SERVER legacy_loopback
    INTO legacy_fdw;

CREATE FOREIGN TABLE IF NOT EXISTS legacy_fdw.crm_accounts_1998 (
    cust_no text NOT NULL,
    company text NOT NULL,
    contact_email text,
    last_invoice_total numeric(12,2) NOT NULL,
    active_flag char(1) NOT NULL,
    loaded_from_file text NOT NULL
)
SERVER legacy_loopback
OPTIONS (schema_name 'legacy', table_name 'crm_accounts_1998');

CREATE FOREIGN TABLE IF NOT EXISTS legacy_fdw.crm_notes_1998 (
    note_no bigint NOT NULL,
    cust_no text NOT NULL,
    note_text text NOT NULL,
    entered_by text NOT NULL,
    entered_on date NOT NULL
)
SERVER legacy_loopback
OPTIONS (schema_name 'legacy', table_name 'crm_notes_1998');

-- Mapped query demo:
-- SELECT m.canonical_customer_ref, f.company, f.last_invoice_total
-- FROM legacy.customer_mappings m
-- JOIN legacy_fdw.crm_accounts_1998 f
--   ON f.cust_no = m.external_customer_ref
-- ORDER BY m.canonical_customer_ref;

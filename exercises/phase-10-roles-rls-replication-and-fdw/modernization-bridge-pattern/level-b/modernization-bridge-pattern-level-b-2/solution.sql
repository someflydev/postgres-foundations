-- Reference shape: import the legacy schema and join local mapping to foreign rows.
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
IMPORT FOREIGN SCHEMA legacy
    LIMIT TO (crm_accounts_1998)
    FROM SERVER legacy_loopback
    INTO legacy_fdw;
SELECT m.canonical_customer_ref, f.company
FROM legacy.customer_mappings m
JOIN legacy_fdw.crm_accounts_1998 f ON f.cust_no = m.external_customer_ref;

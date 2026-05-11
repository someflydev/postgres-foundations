CREATE EXTENSION IF NOT EXISTS postgres_fdw;

SELECT srvname, fdwname
FROM pg_foreign_server s
JOIN pg_foreign_data_wrapper w ON w.oid = s.srvfdw
WHERE srvname = 'legacy_loopback';

IMPORT FOREIGN SCHEMA legacy
    LIMIT TO (legacy_customers)
    FROM SERVER legacy_loopback
    INTO legacy_fdw;

SELECT
    m.canonical_customer_ref,
    f.company AS legacy_company,
    f.last_invoice_total
FROM legacy.customer_mappings AS m
JOIN legacy_fdw.crm_accounts_1998 AS f
    ON f.cust_no = m.external_customer_ref
ORDER BY m.canonical_customer_ref;

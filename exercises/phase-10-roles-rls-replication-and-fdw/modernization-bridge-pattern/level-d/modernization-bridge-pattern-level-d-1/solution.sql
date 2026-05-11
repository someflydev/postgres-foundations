-- Diagnose the original shape.
EXPLAIN (VERBOSE, COSTS OFF)
SELECT *
FROM legacy.customer_mappings AS m
JOIN legacy_fdw.crm_accounts_1998 AS f
    ON lower(f.cust_no) = lower(m.external_customer_ref)
WHERE lower(f.cust_no) = 'c-100';

-- Prefer a predicate that leaves the foreign column raw.
EXPLAIN (VERBOSE, COSTS OFF)
SELECT
    m.canonical_customer_ref,
    f.company,
    f.last_invoice_total
FROM legacy.customer_mappings AS m
JOIN legacy_fdw.crm_accounts_1998 AS f
    ON f.cust_no = m.external_customer_ref
WHERE f.cust_no = 'C-100';

SELECT
    m.canonical_customer_ref,
    f.company,
    f.last_invoice_total
FROM legacy.customer_mappings AS m
JOIN legacy_fdw.crm_accounts_1998 AS f
    ON f.cust_no = m.external_customer_ref
WHERE f.cust_no = 'C-100';

CREATE SCHEMA IF NOT EXISTS legacy_imported;

IMPORT FOREIGN SCHEMA legacy
    LIMIT TO (customers, orders, products)
    FROM SERVER legacy_monolith
    INTO legacy_imported;

REFRESH MATERIALIZED VIEW new_service.legacy_customer_order_totals;

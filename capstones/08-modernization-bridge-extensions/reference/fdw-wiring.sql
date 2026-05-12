CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER legacy_monolith
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'legacy-db.example.internal', dbname 'legacy', port '5432', async_capable 'true');

CREATE USER MAPPING IF NOT EXISTS FOR CURRENT_USER
SERVER legacy_monolith
OPTIONS (user 'bridge_reader', password_required 'false');

IMPORT FOREIGN SCHEMA public
LIMIT TO (customers, invoices)
FROM SERVER legacy_monolith
INTO legacy_fdw;

-- Verify pushdown with EXPLAIN on selective predicates and joins that can run remotely.
-- Use async append when reading independent foreign partitions or compatible foreign tables.

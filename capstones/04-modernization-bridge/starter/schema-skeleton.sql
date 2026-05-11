CREATE SCHEMA legacy_fdw;
CREATE SCHEMA new_service;

-- Add postgres_fdw server, imported legacy tables, local tenant-owned tables,
-- RLS policies, and at least one materialized aggregate cache.

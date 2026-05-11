-- Default Privileges Level C2
-- Repair goal: pair default privileges with explicit `GRANT ... ON ALL ... IN SCHEMA` for existing objects.
ALTER DEFAULT PRIVILEGES FOR ROLE saas_migrations IN SCHEMA saas
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO saas_app_readwrite;
ALTER DEFAULT PRIVILEGES FOR ROLE saas_migrations IN SCHEMA saas
  GRANT USAGE, SELECT ON SEQUENCES TO saas_app_readwrite;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

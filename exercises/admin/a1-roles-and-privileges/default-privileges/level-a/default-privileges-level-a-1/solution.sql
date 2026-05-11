-- Default Privileges Level A1
-- Actor/object/operation review.
ALTER DEFAULT PRIVILEGES FOR ROLE saas_migrations IN SCHEMA saas
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO saas_app_readwrite;
ALTER DEFAULT PRIVILEGES FOR ROLE saas_migrations IN SCHEMA saas
  GRANT USAGE, SELECT ON SEQUENCES TO saas_app_readwrite;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

-- Scenario fragment for Default Privileges.
ALTER DEFAULT PRIVILEGES FOR ROLE saas_migrations IN SCHEMA saas
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO saas_app_readwrite;
ALTER DEFAULT PRIVILEGES FOR ROLE saas_migrations IN SCHEMA saas
  GRANT USAGE, SELECT ON SEQUENCES TO saas_app_readwrite;

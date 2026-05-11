CREATE ROLE saas_app_readwrite NOLOGIN;
CREATE ROLE saas_app_readonly NOLOGIN;
CREATE ROLE saas_migrations NOLOGIN;
CREATE ROLE saas_break_glass NOLOGIN;
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA saas TO saas_app_readwrite;
GRANT SELECT ON ALL TABLES IN SCHEMA saas TO saas_app_readonly;
SELECT grantee, table_schema, table_name, privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'saas'
ORDER BY grantee, table_name, privilege_type;

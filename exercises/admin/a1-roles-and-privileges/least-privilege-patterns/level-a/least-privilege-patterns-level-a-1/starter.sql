-- Scenario fragment for Least Privilege Patterns.
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA saas TO saas_app_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA saas TO saas_app_readwrite;

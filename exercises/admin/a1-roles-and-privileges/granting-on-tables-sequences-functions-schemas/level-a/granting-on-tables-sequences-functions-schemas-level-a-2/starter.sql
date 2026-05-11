-- Scenario fragment for Granting on Tables Sequences Functions Schemas.
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite;
GRANT SELECT, INSERT, UPDATE ON saas.users TO saas_app_readwrite;
GRANT USAGE, SELECT ON SEQUENCE saas.users_id_seq TO saas_app_readwrite;

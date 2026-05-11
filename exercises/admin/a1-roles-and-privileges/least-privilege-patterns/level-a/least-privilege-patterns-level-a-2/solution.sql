-- Least Privilege Patterns Level A2
-- Actor/object/operation review.
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA saas TO saas_app_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA saas TO saas_app_readwrite;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

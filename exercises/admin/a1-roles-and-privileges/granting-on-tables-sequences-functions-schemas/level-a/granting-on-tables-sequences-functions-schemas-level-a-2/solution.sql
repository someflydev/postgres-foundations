-- Granting on Tables Sequences Functions Schemas Level A2
-- Actor/object/operation review.
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite;
GRANT SELECT, INSERT, UPDATE ON saas.users TO saas_app_readwrite;
GRANT USAGE, SELECT ON SEQUENCE saas.users_id_seq TO saas_app_readwrite;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

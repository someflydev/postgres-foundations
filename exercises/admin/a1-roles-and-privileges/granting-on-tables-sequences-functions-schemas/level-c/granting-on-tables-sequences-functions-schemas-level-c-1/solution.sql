-- Granting on Tables Sequences Functions Schemas Level C1
-- Repair goal: audit schemas, tables, sequences, and functions as separate rows in the access review.
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite;
GRANT SELECT, INSERT, UPDATE ON saas.users TO saas_app_readwrite;
GRANT USAGE, SELECT ON SEQUENCE saas.users_id_seq TO saas_app_readwrite;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

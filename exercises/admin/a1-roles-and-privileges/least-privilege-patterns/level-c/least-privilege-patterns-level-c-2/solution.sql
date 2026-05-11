-- Least Privilege Patterns Level C2
-- Repair goal: write the role matrix first, then make every GRANT trace back to one cell in that matrix.
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA saas TO saas_app_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA saas TO saas_app_readwrite;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

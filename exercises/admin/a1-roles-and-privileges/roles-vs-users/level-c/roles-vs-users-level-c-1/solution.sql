-- Roles vs Users Level C1
-- Repair goal: split direct object grants away from login roles and move them to NOLOGIN group roles.
CREATE ROLE saas_app_readwrite NOLOGIN;
CREATE ROLE app_api_login LOGIN;
GRANT saas_app_readwrite TO app_api_login;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

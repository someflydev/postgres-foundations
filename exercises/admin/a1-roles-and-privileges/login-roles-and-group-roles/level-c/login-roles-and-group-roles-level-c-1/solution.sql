-- Login Roles and Group Roles Level C1
-- Repair goal: revoke direct grants from login roles and replace them with membership in named group roles.
CREATE ROLE saas_app_readonly NOLOGIN;
CREATE ROLE bi_reader_login LOGIN;
GRANT saas_app_readonly TO bi_reader_login;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

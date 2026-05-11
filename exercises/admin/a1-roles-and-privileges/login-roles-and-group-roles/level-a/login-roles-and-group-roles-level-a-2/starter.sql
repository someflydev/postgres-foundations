-- Scenario fragment for Login Roles and Group Roles.
CREATE ROLE saas_app_readonly NOLOGIN;
CREATE ROLE bi_reader_login LOGIN;
GRANT saas_app_readonly TO bi_reader_login;

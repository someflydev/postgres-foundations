-- Login Roles and Group Roles Level A1
-- Actor/object/operation review.
CREATE ROLE saas_app_readonly NOLOGIN;
CREATE ROLE bi_reader_login LOGIN;
GRANT saas_app_readonly TO bi_reader_login;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

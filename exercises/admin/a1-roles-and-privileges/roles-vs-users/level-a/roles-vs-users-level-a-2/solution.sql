-- Roles vs Users Level A2
-- Actor/object/operation review.
CREATE ROLE saas_app_readwrite NOLOGIN;
CREATE ROLE app_api_login LOGIN;
GRANT saas_app_readwrite TO app_api_login;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

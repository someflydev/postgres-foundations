-- Scenario fragment for Roles vs Users.
CREATE ROLE saas_app_readwrite NOLOGIN;
CREATE ROLE app_api_login LOGIN;
GRANT saas_app_readwrite TO app_api_login;

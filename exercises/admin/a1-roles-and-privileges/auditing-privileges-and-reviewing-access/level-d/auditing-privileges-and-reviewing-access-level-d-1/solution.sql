REVOKE ALL ON SCHEMA saas FROM app_api_login;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA saas FROM app_api_login;
REVOKE saas_break_glass FROM app_api_login;
GRANT saas_app_readwrite TO app_api_login;

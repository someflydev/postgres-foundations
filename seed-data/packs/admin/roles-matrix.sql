-- Demonstration administration role matrix for the saas domain.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'saas_app_readwrite') THEN
    CREATE ROLE saas_app_readwrite NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'saas_app_readonly') THEN
    CREATE ROLE saas_app_readonly NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'saas_migrations') THEN
    CREATE ROLE saas_migrations NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'saas_break_glass') THEN
    CREATE ROLE saas_break_glass NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_api_login') THEN
    CREATE ROLE app_api_login LOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bi_reader_login') THEN
    CREATE ROLE bi_reader_login LOGIN;
  END IF;
END
$$;

GRANT saas_app_readwrite TO app_api_login;
GRANT saas_app_readonly TO bi_reader_login;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'saas') THEN
    GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA saas TO saas_app_readwrite;
    GRANT SELECT ON ALL TABLES IN SCHEMA saas TO saas_app_readonly;
    GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA saas TO saas_app_readwrite;
    GRANT ALL PRIVILEGES ON SCHEMA saas TO saas_migrations;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA saas TO saas_break_glass;
  END IF;
END
$$;

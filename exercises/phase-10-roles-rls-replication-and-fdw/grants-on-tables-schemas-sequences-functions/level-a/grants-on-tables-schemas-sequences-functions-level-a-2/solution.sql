-- Reference shape: create group roles, then grant membership to login roles.
CREATE ROLE app_reader NOLOGIN;
CREATE ROLE app_writer NOLOGIN;
GRANT USAGE ON SCHEMA saas TO app_reader, app_writer;
GRANT SELECT ON saas.documents TO app_reader;
GRANT SELECT, INSERT, UPDATE ON saas.documents TO app_writer;

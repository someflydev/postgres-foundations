# A1 Roles Playbook

Use roles as the unit of administrative design. PostgreSQL users and groups are
both roles; LOGIN decides whether the role can start a session. Prefer NOLOGIN
group roles for privilege bundles and grant service-specific login roles into
those groups.

Core checklist:

- Grant schema USAGE separately from table privileges.
- Include tables, sequences, and function EXECUTE in reviews.
- Use ALTER DEFAULT PRIVILEGES for future objects only.
- Keep application runtime, migration ownership, BI read-only, and break-glass
  roles separate.
- Review `pg_auth_members`, `information_schema.table_privileges`,
  `pg_namespace` ACL expansion, sequence ACLs from `pg_class`, and function
  ACLs from `pg_proc` after changes.

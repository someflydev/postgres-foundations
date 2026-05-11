# A2 Schemas Playbook

Use schemas for namespaces and grant boundaries inside a database. Use separate
databases only when backup, lifecycle, connection, locale, or isolation needs
justify the extra operational boundary.

Core checklist:

- Default to one database with many schemas for related application data.
- Lock down CREATE on public where older cluster history left it open.
- Treat search_path as executable configuration, especially in privileged
  functions.
- Prefer explicit schema qualification in administrative and security-sensitive
  SQL.
- Choose schema-per-tenant or RLS by tenant count, operational workload, and
  isolation evidence rather than habit.

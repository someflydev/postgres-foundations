# Acceptance Criteria

- DDL applies cleanly to a blank PostgreSQL 16 database.
- Tenant-owned data cannot be read, inserted, updated, or deleted across tenant
  boundaries by ordinary application roles.
- The schema uses constraints to protect business truth instead of relying only
  on application code.
- Indexes are tied to named critical queries and avoid unjustified write cost.
- Critical queries run and stay tenant-scoped.
- Core FTS is implemented for notes.
- JSONB usage is bounded, indexed only when justified, and not used as a hidden
  schema for core CRM facts.
- Audit events are append-only and the retention/partitioning decision is
  explained.
- The runbook is concrete enough for a three-engineer team to operate.
- The writeup defends both chosen and rejected options.

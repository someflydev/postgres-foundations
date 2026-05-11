# Constraints

- PostgreSQL 16.
- No extensions assumed beyond `pgcrypto` and `pg_stat_statements`.
- Single database, single schema, strict RLS for tenant-owned tables.
- Application context uses `current_setting('app.tenant_id', true)` and
  `current_setting('app.user_id', true)`.
- JSONB is allowed only for a bounded `custom_fields` pattern on accounts,
  contacts, or deals.
- Notes require core PostgreSQL full-text search. Do not assume an external
  search service.
- Audit events are append-only with 18 month retention. Discuss partitioning
  and maintenance even if the initial implementation can run unpartitioned.
- Dashboard landing queries target p95 latency below 200 ms at the stated
  growth target.
- Critical queries required:
  1. Tenant dashboard account and open deal summary.
  2. Pipeline by stage.
  3. Recently touched contacts.
  4. Upcoming activities for one user.
  5. Tenant-scoped note full-text search.
  6. Deal detail with account, primary contact, latest note, and activity count.
  7. Custom-field filter on accounts.
  8. Append audit event and inspect recent audit history.
  9. Tenant admin membership and role review.
  10. Audit retention candidates.

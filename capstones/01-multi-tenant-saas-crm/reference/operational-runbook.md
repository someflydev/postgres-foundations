# Operational Runbook

Observe dashboard and search queries through `pg_stat_statements`. Track mean,
p95 from application telemetry, rows returned, shared block reads, and whether
plans use the tenant-leading indexes. Review the top statements weekly during
growth and after adding custom-field filters.

Backups should use the managed provider's continuous backup facility, with a
monthly restore drill into a non-production database. RLS verification belongs
in migrations and smoke tests: create two tenants, set `app.tenant_id`, and
prove each tenant sees only its own rows.

Audit events are append-only. Start unpartitioned if volume is modest, then add
monthly range partitions on `occurred_at` before retention deletes become large
or vacuum-heavy. Retention maintenance should detach or delete data older than
18 months during a low-traffic window and record row counts.

Before adding an index, capture the critical query, expected selectivity, and
write cost. Before dropping an index, confirm it is unused over a representative
period and not serving a rare support workflow.

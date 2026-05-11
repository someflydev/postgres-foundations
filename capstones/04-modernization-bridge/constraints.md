# Constraints

- PostgreSQL 16 on both sides.
- The lab uses the `pg` and `pg-replica` containers as independent databases.
- Use `postgres_fdw` and `IMPORT FOREIGN SCHEMA` for legacy access.
- Use at least one materialized view on the new side for a legacy aggregate.
- Enforce RLS on new-service tenant-owned tables.
- Discuss but do not implement logical replication.
- Do not use Citus; justify why not.

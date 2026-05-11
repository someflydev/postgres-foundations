# Constraints

- PostgreSQL 16.
- No TimescaleDB in the current design.
- Events are partitioned by range on `event_time`.
- Monthly partitions are the reference starting point.
- BRIN on `event_time` and btree on `device_id` per partition are the baseline.
- Retention is eighteen months online, with cold archive after ninety days.
- `pg_stat_statements` is required for operations reasoning.
- Logical replication to a read replica must be considered, not assumed.

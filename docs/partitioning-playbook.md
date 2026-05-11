# Partitioning Playbook

Partitioning is a lifecycle and operations design. Start with the workload,
not the syntax.

## Authoring Steps

1. Name the operational problem: retention, hot/cold separation, vacuum scope,
   bulk load isolation, or bounded maintenance windows.
2. Pick the partition key from real predicates and lifecycle boundaries. For
   event streams this is usually `event_time`; for order history it may be
   `ordered_at`.
3. Choose the strategy. Use range partitioning for time windows, list
   partitioning for stable categories, and hash partitioning only when spreading
   write/read load matters more than lifecycle operations.
4. Create a default partition so unexpected rows have a visible landing zone.
   Alert on rows in the default partition.
5. Create parent-level partitioned indexes, then verify the physical child
   indexes exist. PostgreSQL does not provide a single global index.
6. Check uniqueness rules. A unique constraint on a partitioned parent must
   include every partition key column.
7. Verify pruning with `EXPLAIN`. The predicate should compare the raw
   partition key to constants or stable parameters.
8. Write the retention runbook before production use.

## Range Template

```sql
CREATE TABLE events.event_log_partitioned (
    event_id bigint NOT NULL,
    event_time timestamptz NOT NULL,
    source_id bigint NOT NULL,
    payload jsonb NOT NULL,
    PRIMARY KEY (event_id, event_time)
) PARTITION BY RANGE (event_time);

CREATE TABLE events.event_log_partitioned_2026_05
    PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

CREATE TABLE events.event_log_partitioned_default
    PARTITION OF events.event_log_partitioned DEFAULT;
```

## Retention Template

Create next month's partition before writes need it, then detach the oldest
partition during a planned window:

```sql
ALTER TABLE events.event_log_partitioned
DETACH PARTITION events.event_log_partitioned_2025_05;

CREATE TABLE events.event_log_cold_2025_05
AS SELECT * FROM events.event_log_partitioned_2025_05;

DROP TABLE events.event_log_partitioned_2025_05;
ANALYZE events.event_log_partitioned;
```

For production, wrap this in an idempotent procedure that records the detached
partition name, row count, archive destination, operator, and verification
query. Avoid surprise `ATTACH PARTITION` work on busy tables; validate bounds
with constraints and test lock behavior in a staging database.

## Monthly Checklist

- Future partition exists.
- Default partition is empty or explained.
- Oldest partition is detached or retained by an explicit exception.
- Parent and active child statistics are fresh.
- Date-bounded `EXPLAIN` output prunes to the expected partitions.
- Indexes exist on new partitions.
- Backups and replicas have handled the changed table set.

The right outcome is boring operations. If partitioning adds more work than it
removes, the answer is still "not yet."

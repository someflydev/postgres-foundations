# A4 Backup And Upgrades Playbook

Backup and lifecycle operations are only real when they have been drilled. A
backup artifact, restore command, row-count check, and known-good query belong
in the same runbook entry.

## Backup Choices

Use `pg_dump` for logical, database-level portability and selective restore.
Use `pg_basebackup` plus archived WAL when the recovery target is a physical
cluster timeline and point-in-time recovery matters. Logical backups help with
object movement and version transitions. Physical backups protect the whole
cluster state and require WAL retention discipline.

## pg_dump Practice

Prefer custom format for drills:

```sh
pg_dump -Fc -d "$DATABASE_URL" -f /tmp/pgfound.dump
pg_restore --list /tmp/pgfound.dump
pg_restore -d "$RESTORE_DATABASE_URL" --clean --if-exists /tmp/pgfound.dump
```

Record roles, extensions, schema assumptions, restore duration, row counts, and
critical queries. A dump that has never been restored is unproven.

## Restore Drills

Run the lab drill with:

```sh
scripts/restore-drill.sh
```

The script creates a known probe row, takes a custom-format dump, recreates the
lab database, restores, and asserts the probe query. It is intentionally a lab
operation because it drops and recreates the target database.

## Vacuum And Bloat

Autovacuum workers vacuum dead tuples and analyze tables based on thresholds,
scale factors, and table churn. They cannot clean tuples still visible to a
long-running transaction. Diagnose with `pg_stat_activity`,
`pg_stat_all_tables`, table age, and vacuum/analyze counters. Preview
extensions such as `pgstattuple` only after the core signals show why you need
more detail.

Use plain `VACUUM` to catch up after churn, `VACUUM FREEZE` for wraparound
posture, and `VACUUM FULL` only when the blocking table rewrite is acceptable.

## Statistics Freshness

`ANALYZE` feeds planner estimates. After a bulk load or skew change, stale
statistics can make an index scan, join order, or row estimate look cheaper
than reality. Run targeted `ANALYZE`, compare estimated rows to actual rows,
and keep the evidence with the incident note.

## Major Version Upgrades

`pg_upgrade` is fast when binary compatibility, extensions, collations, and
rollback posture are ready. Logical replication can reduce downtime or move
between platforms, but it introduces dual-running operational work. Upgrade
planning should state compatibility checks, rehearsal results, downtime budget,
rollback plan, and post-upgrade analyze or statistics refresh.

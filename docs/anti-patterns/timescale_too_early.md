# Timescale Too Early

Timescale too early happens when a team adopts TimescaleDB before time-series
analytics is central enough to justify a separate image, extension-specific
operations, licensing review, and managed-service constraints. A timestamp
column or a growing events table is not enough. Phase 9's
`docs/anti-patterns/partition_too_early.md` is the baseline warning: core range
partitioning, BRIN indexes, ordinary materialized views, and retention by
partition detach often solve the first real operational problems.

Use TimescaleDB when the evidence is concrete:

- Time-bucketed analytics dominate the workload.
- Continuous aggregate refresh policy beats a plain materialized view plus a
  scheduler.
- Declarative compression or retention removes real operational toil.
- The team can operate the TimescaleDB image, backups, upgrades, and restore
  drills deliberately.

Treat TimescaleDB as premature when the team cannot name the query latency,
retention, or rollup problem it solves. The repair is usually to stay with core
partitioning, improve indexes and statistics, and revisit TimescaleDB after the
analytics workload is central enough to carry the operational burden.

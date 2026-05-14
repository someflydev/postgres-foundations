# Reference Writeup

## Modeling

This solution keeps the first production version in PostgreSQL core. The event
table is partitioned by range on `event_time` because the dominant reads and the
retention lifecycle are both time-bound. Monthly partitions are a practical
starting point for roughly two million events per day: they keep object counts
manageable while giving the planner a clear pruning boundary for last-day and
seven-day investigations. If a real month becomes too large for maintenance
windows, the next core adjustment is weekly partitions, not an automatic move to
an extension.

## Indexes

The index posture starts deliberately small. BRIN on `event_time` matches an
append-heavy event stream where physical locality mostly follows time. A btree
on `device_id` per partition supports the support engineer's device page and the
seven-day anomaly backtrace. The partial anomaly index is justified only because
anomaly and critical events are the incident path and should be much smaller
than the full stream. Additional payload indexes are deferred until
`pg_stat_statements` shows stable predicates and enough latency pain to justify
the write cost.

Retention is handled by partition maintenance. Data remains online for eighteen
months, but partitions older than ninety days are candidates for cold archive.
The runbook detaches the chosen partition, exports it through the organization's
approved mechanism, and records the archive URI. The key operational property is
that old data leaves the hot partition set without row-by-row deletes, vacuum
storms, or unclear provenance. A production version would dry-run the candidate
list, check for active queries, take an archive checksum, and keep a restore
drill on the calendar.

Logical replication to a read replica is not enabled by default in this
reference design. The support dashboards should first prove their query shape,
partition pruning, and index use on the primary. A replica becomes appropriate
when dashboard reads measurably interfere with ingest or support traffic, when
analytics isolation has a clear owner, and when replica lag is acceptable for
the dashboard promises. A replica will not fix a query that scans all partitions
or wraps predicates so the planner cannot use the intended indexes.

## Extension Posture

`pg_stat_statements` is required because the team needs evidence about query
frequency, latency, rows, and variance. TimescaleDB is deferred. The deferred
decision is not ideological: it preserves portability while the workload can be
served with declarative partitioning, BRIN, btree indexes, and planned retention.
The team should also defer partition-management extensions until maintenance
cadence becomes repetitive enough to justify them.

## When would TimescaleDB be worth it?

TimescaleDB becomes worth evaluating when PostgreSQL core partition maintenance
is the bottleneck rather than the learning curve. Concrete signals include many
more partitions than the team can safely maintain, continuous aggregate needs
that cannot be handled with ordinary materialized views and refresh policy,
compression requirements that materially reduce storage or I/O cost, and
time-series operational expertise on the team. The adoption proposal must also
cover managed-service availability, backup and restore behavior, upgrade
process, and an exit plan for features that create lock-in.

## Operations and Operational Tolerance

The team can operate SQL schema migrations, monthly partition creation, index
checks, and planned detach/export retention. It cannot yet operate a complex
extension stack, unexplained replicas, or dashboard queries that require hero
debugging. The design therefore keeps the moving parts inspectable and makes
future complexity depend on measured signals.

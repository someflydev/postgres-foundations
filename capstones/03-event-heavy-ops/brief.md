# Event-heavy Operations Brief

Build an operational analytics store for a device platform. The system receives
about two million events per day from roughly forty thousand devices. Support
engineers need recent device timelines, anomaly backtraces, severity rollups,
and a repeatable way to investigate slow queries.

Use PostgreSQL 16 core features. Declaratively partition events by range on
event_time, starting with monthly partitions. Begin with BRIN indexes on
event_time and btree indexes on device_id for each partition. Add a partial
index for anomaly and critical events only if you can justify the write cost.

Deliver schema, indexes, critical queries, a retention script, a short slow-query
runbook, and a written defense. The writeup must include a section named "When
would TimescaleDB be worth it?" and must clearly state which extensions are
enabled now, which are deferred, and what measured workload signal would change
that answer.

The answer must also discuss logical replication to an analytics read replica.
State whether to do it now. If the answer is "not yet", name the measurements
that would change the decision. If the answer is "yes", name the operating cost,
failure mode, and query-shape work that still remains.

# Event-heavy Operations Narrative

You are joining the platform team for an IoT-adjacent product used by support
engineers every day. The product receives roughly two million device events per
day from about forty thousand active devices. The support team is not asking for
a research warehouse. They need a dependable operational analytics surface in
PostgreSQL 16 that can answer recent questions quickly, retain history for
eighteen months, and keep the write path understandable for a small operations
team.

The two hottest questions are narrow and time-bound. A support engineer opens a
device page and asks for the last twenty-four hours for that device. During an
incident, the same engineer asks for an anomaly backtrace for that device over
the last seven days. Broader dashboards exist, but they summarize recent
severity and event-type counts for triage. The design should therefore make
device-and-time access cheap without pretending every historical query deserves
the same latency.

The team has heard that TimescaleDB is popular for time-series workloads. In
this capstone, TimescaleDB is not available. That is not a trick and it is not a
value judgment against TimescaleDB. The point is to demonstrate the core
PostgreSQL shape first: declarative range partitioning on event_time, BRIN
indexes for time locality, btree indexes for per-device access, retention
maintenance, and pg_stat_statements-driven observation. Your writeup must state
when TimescaleDB would become worth the additional operational and portability
burden.

Retention is not optional. The business wants eighteen months online, with data
older than ninety days treated as cold. The reference answer keeps monthly
partitions online and demonstrates a detach-and-export posture for older
partitions. The exact archive target is less important than the operational
shape: identify candidate partitions, detach in a planned maintenance window,
export them, record what happened, and prove the hot queries still prune to the
expected partitions.

Logical replication to a read replica is under consideration. Do not add it as a
reflex. The learner must decide whether support dashboards currently justify a
replica and must name the risk that replicas do not fix bad query shapes. The
answer should describe when replica pressure, isolation from dashboard load, or
reporting read volume makes a replica the right next move.

The capstone should feel like production design under constraints. You are not
being asked to chase every possible extension, index, or topology. You are being
asked to build the simplest PostgreSQL design that matches the workload, then
defend where it bends and what evidence would make it evolve.

# E5 TimescaleDB

TimescaleDB is for time-series analytics that has become central to the system,
not for every table with a timestamp. It adds hypertables, chunk management,
continuous aggregates, compression policies, and retention policies, but it also
adds a separate image, extension-specific upgrade posture, licensing review,
and managed-service constraints.

Use the separate `timescale` Compose profile for labs:
`docker compose --profile timescale up -d timescale` from the `docker/`
directory. The image is pinned to `timescale/timescaledb:2.15.3-pg16`. The main
`pg` service remains plain `postgres:16` so Phase 9 partitioning remains a real
core PostgreSQL baseline.

The E5 decision rule is explicit: compare TimescaleDB against core range
partitioning, BRIN indexes, retention by detach or drop, and ordinary
materialized views. Adopt TimescaleDB only when continuous aggregates,
compression, or policy-driven retention materially simplify an important
time-series workload.

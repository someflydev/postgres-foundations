# FDW Without Pushdown Verification

postgres_fdw is useful for migration bridges and bounded federation, but it is still a remote query boundary. If filters, joins, aggregates, or limits do not push down, PostgreSQL may pull far more remote data than the application expects.

This anti-pattern appears when a foreign table becomes a hot path without `EXPLAIN VERBOSE` review. The query looks local in application code, while latency, credentials, remote load, and network transfer become hidden dependencies.

Prefer explicit pushdown verification. Inspect the remote SQL, keep bridge queries narrow, add local materialization when needed, and define when the bridge will be retired or replaced by owned data movement.

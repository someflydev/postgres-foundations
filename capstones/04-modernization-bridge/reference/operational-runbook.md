# FDW Bridge Runbook

1. For slow FDW reads, run `EXPLAIN (VERBOSE)` and check remote SQL pushdown.
2. If the legacy server is unavailable, switch user-facing paths to clear
   degraded behavior rather than silently serving stale direct-read screens.
3. For materialized-view questions, compare the last refresh timestamp with the
   product freshness promise.
4. Validate RLS by setting `app.tenant_id` and proving local rows from another
   tenant are hidden.
5. Escalate to migration planning only when ownership, identifiers, conflict
   handling, and replication operations are ready.

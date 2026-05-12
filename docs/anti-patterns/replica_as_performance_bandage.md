# Replica as Performance Bandage

Read replicas help when a workload can tolerate lag and needs isolation from primary write traffic. They do not fix missing indexes, poor query shapes, excessive row transfer, or application code that performs too many round trips.

The bandage appears when slow primary queries are routed to a replica before plans and indexes are reviewed. The symptom may move away from the primary, but stale reads, lag monitoring, failover routing, and duplicate capacity costs become new operational responsibilities.

Prefer diagnosis first. Use `pg_stat_statements`, `EXPLAIN`, index review, and query-shape changes to reduce avoidable work. Add replicas when the remaining read workload has a clear freshness contract and a runbook for lag, promotion, and routing.

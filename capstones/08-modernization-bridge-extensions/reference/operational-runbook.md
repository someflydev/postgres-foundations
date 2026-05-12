# Operational Runbook

Check pg_stat_statements on the new service and the legacy database. Slow local queries need local plan review. Slow FDW queries need remote plan review, pushdown verification, row estimate checks, and network timing.

Refresh materialized BI views on a schedule that matches reporting freshness. Logical replication feeds the BI replica for read isolation; monitor replication slot lag and publication changes.

Citus is not enabled in the reference design. Revisit only if a distribution key is proven by tenant-local workload, shard-local joins, and single-node limits.

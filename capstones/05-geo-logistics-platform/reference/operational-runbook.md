# Operational Runbook

Start every incident by checking pg_stat_statements for total time, mean time, calls, and rows on the spatial and breadcrumb queries. Confirm whether the slow path is the zone containment query, the breadcrumb replay query, or the SLA aggregation.

For partitions, pg_partman owns future monthly breadcrumb partitions and retention detach operations. Review partition creation before month end, check that inserts route to the current child, and detach old partitions only after cold export succeeds.

For spatial access, inspect GiST index size, vacuum health, and query plans after bulk zone edits. Reindex spatial indexes during a controlled window if bloat or planner drift is measured.

For search, keep delivery notes on core full-text search. Track ranking complaints and missed keyword searches before considering anything semantic.

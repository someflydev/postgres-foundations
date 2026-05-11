# Partition Too Early

Partitioning too early happens when a table is split before the team can name
the operational problem the split solves. A row count alone is not enough.
PostgreSQL can handle many ordinary tables with normal indexes, statistics,
vacuum, and query tuning. Partitioning adds child tables, child indexes,
statistics targets, retention jobs, backup behavior, replica considerations,
and runbook work.

Use partitioning when the evidence is concrete:

- Date-bounded queries routinely prune most data.
- Retention needs detach/drop semantics instead of large deletes.
- Hot and cold data have different maintenance or storage lifecycles.
- Vacuum, index rebuilds, or bulk loads need a smaller operational scope.

Treat partitioning as premature when queries do not include the partition key,
retention is not implemented, partitions are tiny, or the design exists mainly
because the table "might get big someday." The repair is usually to consolidate
back to one table, add the indexes the workload actually needs, and revisit
partitioning after retention or maintenance pain becomes measurable.

The review question is simple: what normal operation becomes safer, smaller, or
more predictable because this table is partitioned?

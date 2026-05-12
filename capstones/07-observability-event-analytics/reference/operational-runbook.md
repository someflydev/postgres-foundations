# Operational Runbook

Use pg_stat_statements to identify dashboard queries that dominate total time and incident queries with high mean time. Check partition pruning before adding indexes.

pg_partman creates daily partitions and handles retention boundaries. Hot partitions stay online for 30 days. Cold partitions are detached, compressed outside the primary path, and retained for six months.

BRIN indexes should stay small. Rebuild or summarize only when plans stop pruning effectively. Logical replication to an analytics replica is appropriate when BI or support workloads interfere with ingest.

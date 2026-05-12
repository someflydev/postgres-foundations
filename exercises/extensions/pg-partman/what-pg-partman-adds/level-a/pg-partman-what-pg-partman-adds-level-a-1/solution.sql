-- One acceptable answer for pg-partman-what-pg-partman-adds-level-a-1.
-- Use pg_partman evidence for automated partition creation, retention, and maintenance on top of core partitioning. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
SELECT partman.run_maintenance_proc();

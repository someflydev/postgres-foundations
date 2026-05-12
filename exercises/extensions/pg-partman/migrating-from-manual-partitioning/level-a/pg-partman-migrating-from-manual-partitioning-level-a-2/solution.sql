-- One acceptable answer for pg-partman-migrating-from-manual-partitioning-level-a-2.
-- Use pg_partman evidence for moving a Phase 9 manual partitioning scheme onto pg_partman without losing data. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
SELECT partman.run_maintenance_proc();

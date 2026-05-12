-- One acceptable answer for pg-partman-operational-rhythm-level-a-2.
-- Use pg_partman evidence for scheduled maintenance and habits that make partition operations boring. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
SELECT partman.run_maintenance_proc();

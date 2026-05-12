-- One acceptable answer for pg-partman-when-pg-partman-is-enough-and-when-to-go-further-level-a-1.
-- Use pg_partman evidence for where pg_partman fits compared with Timescale retention and compression policies. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
SELECT partman.run_maintenance_proc();

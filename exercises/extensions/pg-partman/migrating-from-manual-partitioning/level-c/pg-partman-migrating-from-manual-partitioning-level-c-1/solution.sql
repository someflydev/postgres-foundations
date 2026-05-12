-- One acceptable answer for pg-partman-migrating-from-manual-partitioning-level-c-1.
-- Migrate the phase-09 manual partitioning scheme onto pg_partman without losing data; demonstrate retention and the maintenance procedure.
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
SELECT partman.run_maintenance_proc();

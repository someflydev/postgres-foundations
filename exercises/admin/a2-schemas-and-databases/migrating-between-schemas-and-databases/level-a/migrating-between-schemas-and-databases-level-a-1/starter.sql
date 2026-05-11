-- Scenario fragment for Migrating Between Schemas and Databases.
ALTER TABLE saas.documents SET SCHEMA archive;
-- For a database move, prefer pg_dump custom format and pg_restore into the target.

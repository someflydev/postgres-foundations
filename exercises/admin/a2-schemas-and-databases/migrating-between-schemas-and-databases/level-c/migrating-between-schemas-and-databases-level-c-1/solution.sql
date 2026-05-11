-- Migrating Between Schemas and Databases Level C1
-- Repair goal: inventory dependencies first and verify grants after restore or schema move.
ALTER TABLE saas.documents SET SCHEMA archive;
-- For a database move, prefer pg_dump custom format and pg_restore into the target.
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

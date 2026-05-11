-- Migrating Between Schemas and Databases Level A2
-- Actor/object/operation review.
ALTER TABLE saas.documents SET SCHEMA archive;
-- For a database move, prefer pg_dump custom format and pg_restore into the target.
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

-- Public Schema Discipline Level C2
-- Repair goal: audit `public` ACLs and move application objects into owned schemas.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO PUBLIC;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

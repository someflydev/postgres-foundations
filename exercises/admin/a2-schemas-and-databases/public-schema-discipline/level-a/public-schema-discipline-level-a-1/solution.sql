-- Public Schema Discipline Level A1
-- Actor/object/operation review.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO PUBLIC;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

-- Ownership and Dependent Objects Level C1
-- Repair goal: run an ownership inventory and reassign objects before removing the role.
REASSIGN OWNED BY old_saas_migrations TO saas_migrations;
DROP OWNED BY old_saas_migrations;
DROP ROLE old_saas_migrations;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

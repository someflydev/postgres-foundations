-- Ownership and Dependent Objects Level A1
-- Actor/object/operation review.
REASSIGN OWNED BY old_saas_migrations TO saas_migrations;
DROP OWNED BY old_saas_migrations;
DROP ROLE old_saas_migrations;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

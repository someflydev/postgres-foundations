-- Scenario fragment for Ownership and Dependent Objects.
REASSIGN OWNED BY old_saas_migrations TO saas_migrations;
DROP OWNED BY old_saas_migrations;
DROP ROLE old_saas_migrations;

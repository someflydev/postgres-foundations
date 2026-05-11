-- Scenario fragment for Membership and Inheritance.
CREATE ROLE incident_responder LOGIN NOINHERIT;
GRANT saas_break_glass TO incident_responder;
SET ROLE saas_break_glass;
SELECT current_user, session_user;

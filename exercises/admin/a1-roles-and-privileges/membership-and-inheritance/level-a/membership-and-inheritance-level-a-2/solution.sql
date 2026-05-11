-- Membership and Inheritance Level A2
-- Actor/object/operation review.
CREATE ROLE incident_responder LOGIN NOINHERIT;
GRANT saas_break_glass TO incident_responder;
SET ROLE saas_break_glass;
SELECT current_user, session_user;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

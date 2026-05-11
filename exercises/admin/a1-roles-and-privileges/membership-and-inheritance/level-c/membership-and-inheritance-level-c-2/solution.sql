-- Membership and Inheritance Level C2
-- Repair goal: document role inheritance posture and require explicit `SET ROLE` for elevated groups.
CREATE ROLE incident_responder LOGIN NOINHERIT;
GRANT saas_break_glass TO incident_responder;
SET ROLE saas_break_glass;
SELECT current_user, session_user;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

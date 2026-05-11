-- Auditing Privileges and Reviewing Access Level C2
-- Repair goal: attach catalog query output to a recurring access review and diff it after deployments.
SELECT member_role.rolname AS member, group_role.rolname AS granted_role
FROM pg_auth_members m
JOIN pg_roles member_role ON member_role.oid = m.member
JOIN pg_roles group_role ON group_role.oid = m.roleid;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

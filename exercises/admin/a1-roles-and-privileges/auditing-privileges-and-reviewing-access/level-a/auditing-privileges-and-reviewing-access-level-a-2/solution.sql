-- Auditing Privileges and Reviewing Access Level A2
-- Actor/object/operation review.
SELECT member_role.rolname AS member, group_role.rolname AS granted_role
FROM pg_auth_members m
JOIN pg_roles member_role ON member_role.oid = m.member
JOIN pg_roles group_role ON group_role.oid = m.roleid;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

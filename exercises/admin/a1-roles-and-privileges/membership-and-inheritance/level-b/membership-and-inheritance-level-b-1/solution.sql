-- Membership and Inheritance Level B1
SELECT member_role.rolname AS member, group_role.rolname AS granted_role
FROM pg_auth_members membership
JOIN pg_roles member_role ON member_role.oid = membership.member
JOIN pg_roles group_role ON group_role.oid = membership.roleid
ORDER BY member, granted_role;

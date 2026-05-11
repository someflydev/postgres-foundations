-- Role memberships.
SELECT member_role.rolname AS member, group_role.rolname AS granted_role
FROM pg_auth_members membership
JOIN pg_roles member_role ON member_role.oid = membership.member
JOIN pg_roles group_role ON group_role.oid = membership.roleid
ORDER BY member, granted_role;

-- Schema privileges.
SELECT
  grantee.rolname AS grantee,
  namespace.nspname AS schema_name,
  privilege.privilege_type
FROM pg_namespace namespace
CROSS JOIN LATERAL aclexplode(namespace.nspacl) AS privilege
JOIN pg_roles grantee ON grantee.oid = privilege.grantee
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY grantee, schema_name, privilege_type;

-- Table privileges.
SELECT grantee, table_schema, table_name, privilege_type
FROM information_schema.table_privileges
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY grantee, table_schema, table_name, privilege_type;

-- Sequence privileges.
SELECT
  grantee.rolname AS grantee,
  namespace.nspname AS sequence_schema,
  sequence.relname AS sequence_name,
  privilege.privilege_type
FROM pg_class sequence
JOIN pg_namespace namespace ON namespace.oid = sequence.relnamespace
CROSS JOIN LATERAL aclexplode(sequence.relacl) AS privilege
JOIN pg_roles grantee ON grantee.oid = privilege.grantee
WHERE sequence.relkind = 'S'
ORDER BY grantee, sequence_schema, sequence_name, privilege_type;

-- Function privileges.
SELECT
  grantee.rolname AS grantee,
  namespace.nspname AS function_schema,
  routine.proname AS function_name,
  privilege.privilege_type
FROM pg_proc routine
JOIN pg_namespace namespace ON namespace.oid = routine.pronamespace
CROSS JOIN LATERAL aclexplode(routine.proacl) AS privilege
JOIN pg_roles grantee ON grantee.oid = privilege.grantee
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY grantee, function_schema, function_name, privilege_type;

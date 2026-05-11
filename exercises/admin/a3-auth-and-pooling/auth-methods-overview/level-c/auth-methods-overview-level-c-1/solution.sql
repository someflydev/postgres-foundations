-- One acceptable answer for auth-methods-overview-level-c-1.
-- Evidence: inspect the relevant PostgreSQL view or command output before changing state.
SELECT current_database(), current_user;
-- Action: apply the smallest scoped remediation described in the prompt.
-- Verification: repeat the evidence query and document the changed result.

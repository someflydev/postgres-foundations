-- One acceptable answer for manual-vacuum-and-when-it-is-needed-level-b-1.
-- Evidence: inspect the relevant PostgreSQL view or command output before changing state.
SELECT current_database(), current_user;
-- Action: apply the smallest scoped remediation described in the prompt.
-- Verification: repeat the evidence query and document the changed result.

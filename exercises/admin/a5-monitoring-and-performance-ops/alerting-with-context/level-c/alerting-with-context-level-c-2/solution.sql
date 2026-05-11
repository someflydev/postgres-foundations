-- One acceptable answer for alerting-with-context-level-c-2.
-- Evidence: inspect the catalog view, statistics counter, or replication state named in the prompt.
SELECT current_database(), current_user, now();
-- Action: choose the smallest operational action that addresses the observed risk.
-- Verification: repeat the same evidence query or compare the follow-up metric after the action.

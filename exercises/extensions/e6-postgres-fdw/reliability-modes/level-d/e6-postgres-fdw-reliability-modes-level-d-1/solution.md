# Solution

Treat the slow foreign server as an operational dependency. Use pg_stat_activity to show waiting sessions, set a bounded statement_timeout for the federation path, and describe an application circuit-breaker pattern that stops repeatedly sending traffic to a failing remote system. Include the pg_sleep trigger or equivalent slow-remote setup in the diagnosis narrative.

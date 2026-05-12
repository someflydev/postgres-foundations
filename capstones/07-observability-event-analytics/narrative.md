# Observability Event Analytics

An internal platform team receives events from 500 services at roughly 300 million events per day. Support engineers need recent dashboards and ad-hoc incident backtraces. Hot retention is 30 days and cold retention is six months.

This capstone asks for an honest PostgreSQL design. Core partitioning, BRIN, and pg_partman are required. TimescaleDB is a decision to argue, not a default answer.

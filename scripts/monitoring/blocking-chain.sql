-- Purpose: show waiting sessions and the sessions currently blocking them.
-- Run during an incident or blocking drill to decide which backend owns the queue.
SELECT
    waiting.pid AS waiting_pid,
    waiting.usename AS waiting_user,
    waiting.state AS waiting_state,
    waiting.wait_event_type,
    waiting.wait_event,
    blocker.pid AS blocking_pid,
    blocker.usename AS blocking_user,
    blocker.state AS blocking_state,
    age(clock_timestamp(), waiting.query_start) AS waiting_for,
    left(waiting.query, 140) AS waiting_query,
    left(blocker.query, 140) AS blocking_query
FROM pg_stat_activity AS waiting
JOIN LATERAL unnest(pg_blocking_pids(waiting.pid)) AS blocked_by(pid) ON true
JOIN pg_stat_activity AS blocker ON blocker.pid = blocked_by.pid
ORDER BY waiting.query_start NULLS LAST;

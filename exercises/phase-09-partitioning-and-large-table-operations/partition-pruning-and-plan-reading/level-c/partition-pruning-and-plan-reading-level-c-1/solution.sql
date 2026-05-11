DROP TABLE IF EXISTS events.partition_pruning_drill CASCADE;
CREATE TABLE events.partition_pruning_drill (
    event_id bigint NOT NULL,
    source_id bigint NOT NULL,
    event_time timestamptz NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (event_id, event_time)
) PARTITION BY RANGE (event_time);
CREATE TABLE events.partition_pruning_drill_2025_11
    PARTITION OF events.partition_pruning_drill
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE events.partition_pruning_drill_default
    PARTITION OF events.partition_pruning_drill DEFAULT;
INSERT INTO events.partition_pruning_drill (event_id, source_id, event_time, payload)
VALUES
    (1, 1, '2025-11-03 10:00:00+00', '{"drill": 1}'::jsonb),
    (2, 1, '2025-11-14 11:00:00+00', '{"drill": 2}'::jsonb),
    (3, 1, '2025-11-28 12:00:00+00', '{"drill": 3}'::jsonb);
EXPLAIN
SELECT count(*)
FROM events.partition_pruning_drill
WHERE event_time >= '2025-11-01'::timestamptz
  AND event_time < '2025-12-01'::timestamptz;
EXPLAIN
SELECT count(*)
FROM events.events
WHERE occurred_at >= '2025-11-01'::timestamptz
  AND occurred_at < '2025-12-01'::timestamptz;

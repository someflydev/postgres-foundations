CREATE INDEX IF NOT EXISTS event_windows_window_gist_verify_idx
ON events.event_windows USING gist ("window");
ANALYZE events.event_windows;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, label
FROM events.event_windows
WHERE "window" && tstzrange('2026-03-01 12:00:00+00', '2026-03-01 12:10:00+00', '[)');

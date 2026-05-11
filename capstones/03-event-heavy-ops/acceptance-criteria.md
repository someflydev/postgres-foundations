# Acceptance Criteria

- Schema applies cleanly and uses declarative partitioning for events.
- Index plan starts with BRIN on time and btree on device per partition.
- Critical queries include top-N recent anomaly devices and device timeline.
- Retention script demonstrates detach and archive bookkeeping.
- Runbook starts from a slow-query symptom and uses plan and statistics evidence.
- Writeup includes an explicit extension posture and TimescaleDB-later criteria.

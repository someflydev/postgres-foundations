# Operational Runbook

The booking path should treat SQLSTATE `23P01` from the exclusion constraint as
a normal conflict: rollback, refresh availability, and ask the patient to pick a
different slot. The application may retry only when it can choose a different
candidate slot; blind retry of the same range should not loop.

Track booking attempts, conflict counts, cancellation counts, and waitlist
promotion latency. Use `pg_stat_statements` to watch availability, upcoming
booking, and waitlist queries. Restore drills should include appointments and
waitlist entries because they are the correctness-critical records.

Time-zone regression tests should cover daylight-saving transitions and
providers in each supported zone. Appointments remain `timestamptz`; local
display is a rendering concern tied to the professional timezone.

Do not partition appointments at the pilot scale. Revisit when retention,
archive, or query plans show that date-bounded operations dominate table access.
Do not add PostGIS until product requirements include distance ranking or
geographic containment that region filters cannot handle.

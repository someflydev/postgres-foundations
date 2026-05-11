# Acceptance Criteria

- DDL applies cleanly to a blank PostgreSQL 16 database.
- Overlapping confirmed appointments for one professional are impossible.
- Cancelled appointments no longer block the slot.
- Availability and blackout data can be queried for a provider and local date
  range.
- Critical queries run without syntax errors.
- The concurrency scenario shows one of two concurrent overlapping bookings
  fails with an exclusion violation.
- Time-zone assumptions are explicit and use `timestamptz` for appointment
  instants.
- The indexing plan is tied to the named workflows.
- The runbook handles conflict retries, waitlist promotion, and operational
  checks.
- The writeup defends deferred PostGIS and deferred partitioning.

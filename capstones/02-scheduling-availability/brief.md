# Brief

Produce a PostgreSQL 16 design for a multi-region healthcare scheduling
platform. Your submission must include schema DDL, index DDL, critical queries,
a concurrency scenario, an operational runbook, and a written defense. Treat the
capstone as a correctness exercise first. A reviewer should be able to see how
the schema represents scheduling facts, how it prevents overlapping confirmed
appointments, and how the team would operate the design during a live pilot.

The schema must model practices, professionals, patients, provider availability
templates, blackout windows, appointments, cancellations, and waitlist entries.
Confirmed appointments for a provider must not overlap. Enforce that rule at
the database layer with an exclusion constraint over a `tstzrange`. The design
should allow cancelled appointments to remain in history without continuing to
block the time range. Use constraints to protect status values, non-empty time
ranges, and required relationships.

Availability templates should use multirange values to represent recurring
local-time windows. You may keep template expansion simple, but you must explain
how local windows become candidate `timestamptz` appointment ranges for a
specific provider timezone. Blackout windows should be concrete timestamp
ranges, because exceptions occur at real instants. Your writeup must explain how
provider time zones affect local-day queries and display.

Write the critical queries named in `constraints.md`: provider availability,
booking, upcoming bookings, cancellation plus waitlist promotion, waitlist
inspection, optional FTS over professional bios and specialties, and the
partitioning decision. Queries should be runnable and should use clear
parameters or CTEs so a reviewer can adapt them for local testing.

The concurrency scenario must demonstrate that two sessions attempting to book
the same provider slot cannot both succeed. If the loser receives SQLSTATE
`23P01`, that is a successful demonstration of the database invariant. The
application can handle that error as a normal booking conflict.

Your indexes should be tied to the named workflows: provider availability,
blackout overlap checks, upcoming confirmed appointments, waitlist promotion,
and optional professional search. Do not partition appointments merely because
time is involved. Explain why partitioning is likely premature for 200
professionals and what volume, retention, or maintenance signal would change
that decision.

Your runbook should cover booking conflict errors, retry behavior, observation,
backup and restore, time-zone regression checks, and waitlist maintenance. Your
writeup must explain why the design uses exclusion constraints, why PostGIS is
not yet justified, and why appointment partitioning is likely premature at the
stated scale.

Submit the artifacts as a reviewer-ready package. The DDL should apply cleanly
to a blank PostgreSQL 16 database. The exclusion constraint should be visible
and named clearly enough that a reviewer can connect it to the double-booking
requirement. The critical queries should avoid hidden assumptions about local
time. If a query is only a simplified reference shape, say what production code
would add rather than pretending the simplification is complete.

Your operational defense should include normal failure paths. A booking conflict
is not an outage; it is an expected result of concurrent demand. A stale
availability display is not ideal, but it is tolerable when the final insert is
protected. A missed waitlist promotion, on the other hand, may be a workflow
defect that needs alerting or retry. Use those distinctions to explain what the
team should measure.

The reviewer will score the design on correctness, not novelty. A smaller
schema with a sound exclusion constraint, clear time-zone reasoning, and a
credible runbook is better than a broad scheduling platform that cannot prove
two overlapping confirmed appointments are impossible.

Your writeup should include a short extension posture. Name the extensions you
enable now, why they are justified, and which ones you explicitly defer.
`btree_gist` is expected because it supports the exclusion constraint. PostGIS
is not expected because the scenario does not require distance or containment
queries. If you choose to implement full-text search, keep it proportional to
the pilot and explain how it would be revisited if search quality became a
product differentiator.

# Reference Writeup

## Position

The design makes the database responsible for the rule that matters most: a
professional cannot have overlapping confirmed appointments. The application
can search, suggest, pre-check, retry, and explain conflicts, but the database
must be the final authority on confirmed schedule state. This is exactly the
kind of invariant PostgreSQL range types and exclusion constraints are meant to
protect.

The core appointment table stores a `tstzrange` named `slot`. The exclusion
constraint compares `(professional_id WITH =, slot WITH &&)` and applies only
where `status = 'confirmed'`. That partial predicate is important. It means a
cancelled appointment can remain in the table for history and support review
without continuing to block the provider's time. It also keeps the rule focused
on the state that matters for double-booking.

`btree_gist` is enabled because GiST needs equality support for the provider
identifier inside the exclusion constraint. This is a modest, well-understood
extension choice. It is available in managed PostgreSQL environments and
directly supports a correctness requirement. The design does not add PostGIS,
TimescaleDB, or a search extension because the stated pilot does not need those
capabilities.

## Schema choices

Practices group professionals. Professionals carry a display name, timezone,
specialties, bio, and optional search vector. Patients carry identity and
contact information. Availability templates belong to professionals and use a
`tsmultirange` for recurring local windows on a day of week during an effective
date range. Blackout windows are concrete `tstzrange` values. Appointments are
concrete commitments between a professional, a patient, and a timestamp range.
Waitlist entries represent patient intent and ordering for future promotion.

This separation avoids mixing usual availability, exceptions, and bookings into
one table. A recurring template says what is normally possible. A blackout says
what is temporarily impossible. A confirmed appointment says what is already
committed. A waitlist entry says who should be contacted if a slot opens. These
facts change on different timelines and have different integrity rules, so they
deserve separate tables.

The availability template uses local-time multiranges because providers and
admins think in local working windows: Monday 09:00-12:00 and 13:00-16:00, for
example. The appointment table uses `tstzrange` because a booking is a real
instant range. Template expansion is the bridge between those two ideas. The
application, or a future database helper, should combine the provider timezone,
the requested local date, and the local template windows to produce candidate
`tstzrange` values. Those candidates must then be filtered against blackout
windows and confirmed appointments.

## Concurrency correctness

The exclusion constraint handles the race where two patients try to book the
same provider slot at the same time. Without the constraint, both sessions can
read an apparently open slot and both can insert. With the constraint, one
insert wins and the conflicting insert fails with SQLSTATE `23P01` once
PostgreSQL can determine the conflict. The application should treat that error
as a normal booking conflict: roll back, refresh availability, and ask the
patient to choose another slot.

This is stronger than an application-level pre-check. A pre-check is still
useful for user experience, but it is not a correctness boundary. It can be
stale before the insert runs. It can be skipped by a maintenance script. It can
be wrong during retries. The exclusion constraint is attached to the data and
therefore protects every write path that attempts to create a confirmed
overlap.

Cancelled appointments no longer block because the exclusion predicate is
limited to `status = 'confirmed'`. That means cancellation is a state transition
instead of a delete. Keeping the row supports auditability and support
questions: the team can answer what was booked, when it was cancelled, and what
happened afterward. A production design might add a cancellation reason and
actor, but the reference schema keeps the core shape small.

## Time-zone handling

Appointments are stored as `tstzrange`, not as local timestamps. This choice
protects real instants and makes overlap checks meaningful. The provider's
timezone is stored separately for rendering and local-day queries. When the UI
asks for a provider's Monday availability, the system must interpret Monday in
that provider's timezone, expand local template windows, and then convert the
candidate ranges to `tstzrange` values.

The design should be tested around daylight-saving transitions. Some local
times do not exist, and some occur twice. PostgreSQL can represent the resulting
instants, but the product must have a policy for ambiguous or skipped local
times. For a pilot, the simplest operational rule is to avoid generating slots
inside known transition gaps and to include regression tests for each supported
timezone.

## Query and index strategy

Availability lookup starts from `professional_id` and `day_of_week`, then
checks effective dates. Blackout checks need overlap search, so the reference
uses a GiST index on professional and slot. Upcoming bookings use a partial
B-tree index on `(professional_id, lower(slot))` for confirmed appointments.
Waitlist promotion uses provider and creation time for waiting entries.
Optional professional search uses a GIN index on `search_vector`.

The exclusion constraint itself is not just an index optimization; it is an
integrity rule. The supporting query indexes are still useful because users
will repeatedly load provider calendars, appointment lists, and waitlists. Each
index has a named workflow. The design avoids indexing every timestamp and
status column independently because that would add write cost without a clear
read path.

The optional full-text search is intentionally secondary. Professional bios and
specialties can be searched with core PostgreSQL FTS if the product wants basic
matching. The reference keeps the search vector as a normal maintained column
rather than a generated expression over an array because PostgreSQL immutability
rules make some generated expressions unsuitable. In a production application,
the write path or a trigger could maintain this vector.

## Partitioning and extension posture

Appointments are not partitioned yet. Two hundred professionals across a pilot
does not imply a large enough appointment table to justify partition
maintenance. The hot queries are provider-bounded and time-ordered, which the
partial B-tree index supports. Partitioning becomes worth reconsidering if
appointment volume grows dramatically, retention policies require fast archival
by date, maintenance on old rows interferes with normal operations, or query
plans show persistent date-pruning benefits that ordinary indexes cannot
provide.

PostGIS is also deferred. The product filters by practice and region, not by
distance, drive time, or geographic containment. Adding PostGIS now would create
modeling and operational work without serving a stated requirement. If future
product requirements include distance-ranked provider search, service areas,
or geo-fenced scheduling, the team should revisit that decision with real query
examples.

The extension posture is therefore narrow. Use `btree_gist` because it directly
supports the exclusion constraint. Use `pgcrypto` if UUID generation is needed.
Use `pg_stat_statements` for observation. Defer other extensions until the team
can name the workload signal and operational owner.

## Operations

The booking path should record conflict rates. A sudden rise in `23P01`
conflicts could be normal during high demand, or it could indicate stale
availability caching. The application should not blindly retry the same slot.
It should refresh candidate availability and ask the patient to select another
time. Support tooling should make it easy to inspect a provider's confirmed
appointments, blackouts, and waitlist entries for a date range.

Backups and restore drills matter because appointment history and waitlist
state are operationally sensitive. A restored environment should be able to
answer upcoming bookings and waitlist order. Observability should include slow
calendar queries, booking attempts, conflicts, cancellations, and waitlist
promotion latency.

Waitlist promotion is shown as a query pattern rather than a full workflow.
That is appropriate for the capstone. A production system would add
notification state, offer expiration, idempotency keys, and possibly row locks
when selecting the next waiting patient. The important point is that waitlist
intent is separate from appointment confirmation. A patient is not booked until
an appointment insert or update succeeds under the same exclusion rule.

This design stays close to PostgreSQL core and uses one targeted extension for
the correctness invariant. It gives the pilot a reliable scheduling foundation
without pretending that search, geo, or partitioning problems have already
arrived.

## Availability expansion detail

The reference schema does not fully implement slot generation because the
capstone is about database design and correctness boundaries, not building a
complete calendar engine. The intended workflow is still clear. For a provider
and local date, find matching availability templates by day of week and
effective date. Interpret each local multirange element in the provider's
timezone. Convert each candidate local window into a concrete `tstzrange`.
Subtract blackout windows and existing confirmed appointments. Present the
remaining ranges to the patient, usually split into appointment-sized slots by
application code.

This split is deliberate. Templates are recurring local business rules.
Blackouts and appointments are real timestamp ranges. Keeping those layers
separate makes it possible to explain why a provider is normally available but
not available on a specific day. It also lets the product add appointment-type
duration rules later without changing the basic invariant that confirmed
appointment ranges cannot overlap.

## Cancellation and waitlist posture

Cancellation is a state transition on appointments. It records that a
previously confirmed slot is no longer active. Because the exclusion constraint
only applies to confirmed rows, the slot becomes available for another booking
after cancellation. The waitlist query in the reference solution promotes the
oldest waiting entry for the professional to an offered state. It does not
pretend that an offer is the same thing as a booking.

That distinction matters operationally. A waitlisted patient may decline, fail
to respond, or need a different appointment type. A production workflow should
track offer expiration, notification attempts, and idempotency keys. It may use
`SELECT ... FOR UPDATE SKIP LOCKED` when multiple workers promote waitlist
entries. The capstone reference leaves those details as future workflow work
while preserving the core data boundary: a patient is not confirmed until an
appointment row satisfies the exclusion constraint.

## Error handling and retries

The application should treat `23P01` as a domain error for booking conflicts.
It should not show a raw database message to patients, and it should not retry
the identical insert in a tight loop. The correct response is to roll back,
refresh available slots for the provider, and ask the patient to choose again.
If conflicts spike, the team should inspect whether the UI is caching
availability too aggressively or whether high-demand providers need shorter
reservation holds or a queueing workflow.

Other errors have different meaning. A foreign key error may mean the patient
or provider id is stale. A range check failure means the application generated
an invalid slot. A timezone conversion bug may show up as slots at impossible
local times. The runbook should distinguish these categories because treating
every booking failure as "try again" would hide data and application defects.

## Data retention and history

The reference schema keeps appointment rows after cancellation because support
and clinical operations often need history. A future retention policy may
archive old completed or cancelled appointments, but that is separate from
partitioning. The pilot should first establish how long practices need
appointment history online, what audit obligations apply, and how often old
appointments are queried. Only then should the team decide whether archival
tables, partitions, or provider-scoped summaries are worth the extra operations.

Waitlist entries also deserve retention thought. A short-lived waitlist entry
may still explain why a patient received an offer. The capstone does not require
a complete compliance policy, but it does expect the learner to notice that
healthcare scheduling data is operationally sensitive. Backup and restore
drills should include appointments, cancellations, and waitlists together
because restoring only one part of the workflow would produce confusing state.

## Search and geography

The professional search vector is optional because search quality is not the
main correctness risk. If the product team wants basic specialty matching, core
PostgreSQL FTS is sufficient for the pilot. A maintained `tsvector` column plus
a GIN index can support simple search without adding another service. If search
later needs synonyms, ranking tuning, typo tolerance, or separate indexing
lifecycles, the team can evaluate other options with actual search logs.

PostGIS is deferred for the same reason. Region and practice filters can be
modeled with ordinary columns. Distance ranking, drive-time estimates, or
service-area containment would change that decision, but those are not in the
pilot scope. Adding PostGIS before those requirements exist would make the
schema look more advanced without improving scheduling correctness.

## Testing posture

The most important automated test is the race. Two sessions attempt to book the
same professional and slot. One succeeds. The other fails. This should be part
of the capstone because it proves the database invariant in a way a single
query cannot. Additional tests should cover cancelled appointments no longer
blocking a slot, blackout overlap filtering, provider local-day lookup, and
daylight-saving transition behavior.

Manual review should inspect the exclusion constraint predicate. A common bug is
to apply an exclusion constraint to all appointment rows, which makes cancelled
appointments block forever. Another bug is to omit the provider equality term,
which would make different providers conflict with each other. A third bug is
to store local timestamps and then compare ranges across time zones incorrectly.
The reference design avoids those mistakes by making each rule explicit.

## Final defense

The capstone's answer is intentionally narrow. It does not build every feature
that a mature healthcare scheduler might need. It builds the foundation that
the pilot cannot safely live without: concrete appointment ranges, provider
timezones, recurring availability, blackout exceptions, waitlist intent, and a
database-enforced no-overlap rule. It names the places where future product
requirements would change the design, and it refuses to adopt heavier
extensions before those requirements arrive. That is the right posture for a
small team shipping a correctness-sensitive pilot.

A reviewer should also notice what the design does not claim. It does not
guarantee that the user interface always displays perfectly fresh availability.
It guarantees that the final confirmation write cannot violate provider
schedule truth. It does not implement every waitlist notification rule. It
keeps waitlist state separate so those rules can be added without weakening the
appointment invariant. It does not solve geographic discovery. It states the
signals that would justify that work later.

The same reasoning applies to appointment types and resources. A future version
may need thirty-minute visits, hour-long intakes, rooms, equipment, or provider
pools. Those requirements would add tables and constraints, but they would not
remove the need for a concrete booked range and a no-overlap rule for whichever
resource is exclusive. Starting with professional exclusivity gives the pilot a
clear invariant and a natural path to generalize if the product proves the need.

Finally, the design is reviewable. The exclusion constraint is visible in the
DDL. The indexes have named workflows. Time-zone assumptions are explicit. The
runbook tells the application how to treat conflicts. The concurrency scenario
proves the race behavior rather than merely describing it. That is what makes
the submission capstone-quality: it connects database mechanics to user-facing
correctness and operational practice.

The result is intentionally practical. A small team can run it, explain it to
practice stakeholders, and extend it when real scheduling complexity appears.

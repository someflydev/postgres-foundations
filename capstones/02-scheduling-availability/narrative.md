# Scheduling and Availability Narrative

The product is a patient self-scheduling platform for healthcare practices
spread across three time zones. The first rollout supports 200 professionals:
physicians, nurse practitioners, therapists, and lab staff. Patients search for
a professional, choose a time, and receive a confirmed appointment. Practice
admins maintain recurring availability templates and one-off blackout windows.
When a patient cancels, the system should make it easy to promote the next
patient on the waitlist.

The team is not trying to build a national marketplace on day one. It is
serving a controlled pilot across a handful of practices, each with known
providers and known regions. The hard part is not internet-scale discovery. The
hard part is correctness under ordinary pressure. Two patients may try to book
the same slot at the same time. A provider may be available every Tuesday
morning except during a conference week. A patient may cancel a slot that
another patient has been waiting for. The database design must protect those
facts even when application code is busy, retried, or wrong.

Double-booking must be impossible at the database layer. The application can
pre-check availability, show friendly errors, and retry workflows, but it is
not allowed to be the final authority on whether two confirmed appointments
overlap. If two sessions race for the same professional and time range, one of
them must fail. That failure should be a normal, observable booking conflict,
not a rare mystery. The product team would rather handle a clean conflict error
than discover overlapping confirmed visits during a morning clinic.

Time zones are part of the domain. Providers work in local schedules, and
patients think in local appointment times. The database should store appointment
instants as `timestamptz` and retain each provider's timezone for rendering and
local-day calculations. It should not pretend that a local date is globally
meaningful. A provider in Phoenix and a provider in New York can both have an
8:30 AM template, but those local windows map to different UTC instants. The
design should be especially careful around daylight-saving transitions and
around queries that ask for "Monday" in a provider's location.

Availability has two layers. Recurring templates describe when a provider
usually accepts appointments. Blackout windows describe concrete exceptions:
vacation, conferences, administrative blocks, emergency closures, or practice
holidays. Appointments are concrete commitments. Waitlist entries are patient
intent, not bookings. A good design keeps those facts separate so the product
can answer questions like "When is this provider usually available?", "What
concrete slots are blocked next week?", "What appointments are already
confirmed?", and "Who should be offered this cancelled slot?"

The team is small and the deployment target is ordinary managed PostgreSQL.
Use PostgreSQL 16 features that fit the problem: range types, exclusion
constraints, multiranges for templates, indexes, and clear transaction
behavior. `btree_gist` is acceptable because the exclusion constraint needs
GiST equality support on a provider identifier. Do not add PostGIS yet. The
current product filters by region and practice, not precise patient distance,
so geographic indexing would add operational and modeling burden before it
solves a measured problem.

Full-text search on professional bios and specialties is useful but not the
central risk. If implemented, it should use core PostgreSQL search and stay
secondary to scheduling correctness. The platform can survive a basic search
experience during the pilot. It cannot survive unreliable appointment
confirmation.

The deadline is a pilot with three practices in eight weeks. Reviewers should
be able to apply the DDL, inspect the exclusion constraint, run the critical
queries, and execute a concurrency scenario that demonstrates the double-booking
protection. The desired outcome is a database design that makes the most
important failure mode boring: one booking succeeds, the conflicting booking
fails, and the application has a clear path to tell the patient what happened.

The pilot team also wants a design that will not corner them if scheduling gets
more sophisticated. Practices may later ask for appointment types with different
durations, provider pools, rooms, equipment, intake forms, insurance rules, or
distance-based search. Those are plausible future requirements, but they should
not be smuggled into the first schema as half-built complexity. The capstone
should solve the stated problem completely and identify the decision points
where those future requirements would change the model.

Operationally, assume the support team will debug real patient complaints. They
will need to answer why a slot disappeared, whether a cancellation promoted a
waitlisted patient, and why a patient saw a conflict after clicking a time. The
database design should leave enough history and structure to answer those
questions without treating every incident as a forensic investigation.

The product leadership is asking for confidence, not a large architecture
diagram. They want to know that the same provider cannot be promised to two
patients at once, that local times are not silently shifted, and that normal
booking conflicts are handled as product events rather than outages. The
engineering team wants a design that can be explained during review and operated
with ordinary PostgreSQL skills. That combination makes this a capstone: the
right answer requires schema modeling, constraints, indexes, transaction
thinking, time-zone discipline, and a written argument for what should wait.

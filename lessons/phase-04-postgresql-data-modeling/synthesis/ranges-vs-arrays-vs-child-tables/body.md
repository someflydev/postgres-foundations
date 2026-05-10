# Ranges vs Arrays vs Child Tables

## Problem Framing

Ranges vs Arrays vs Child Tables belongs in Phase 4b because PostgreSQL-specific types should solve a
specific modeling problem, not decorate a schema. The concrete topic is deciding between tags, slots, multiranges, and child rows.
A good-fit example is matching tags, intervals, calendars, and lifecycle facts to different shapes. A bad-fit example is choosing one flexible type for every repeating or time-shaped fact. The learner should
leave this lesson able to explain which fact is being modeled, which queries
become simpler, and which future maintenance task becomes less fragile.

The pressure in this phase is representation. Arrays, ranges, and multiranges
all describe more than one scalar value, but they do not describe the same kind
of truth. An array says a small bounded set belongs to the row. A range says one
continuous interval has lower and upper bounds. A multirange says a value can be
made of several non-overlapping intervals. A child table says the repeating
member is a row with its own lifecycle. Good design starts by naming that
difference before writing syntax.

## Minimal Concept Introduction

The minimal habit is to ask what PostgreSQL can enforce and compare directly.
For arrays, membership and containment are useful when the elements are labels
and the list remains small. For ranges, operators such as overlap and
containment remove hand-written interval arithmetic. For multiranges, calendar
math can stay in the database without pretending every schedule is one
continuous block. These choices are PostgreSQL core features and are available
in the lab's PostgreSQL 16 server.

This lesson still keeps the not-yet boundary visible. CTEs, window functions,
lateral joins, recursive queries, upserts as a topic, views, materialized views,
partitioning, and implementation-level index tuning remain later work. The
lesson may mention GIN for array and JSONB containment and GiST for ranges and
exclusion constraints, but it treats them as pointers. The first responsibility
is to choose the right shape.

## Worked Example

Use deciding between tags, slots, multiranges, and child rows. In the good-fit design, the column or table expresses the business
rule without asking application code to remember hidden conventions. Queries can
read the model directly, reviewers can see the invariant, and migrations have a
clear target if the workload grows. When a product has a handful of labels,
`tags text[]` is understandable. When a professional has a booking slot,
`tstzrange` carries both endpoints and bound semantics. When availability has
several separated windows, `tstzmultirange` is a better fit than scattered
columns.

The bad-fit redesign chooses the convenient container and ignores lifecycle.
For example, stuffing grants into `roles text[]` loses who granted a role and
when it was revoked. Modeling price history as a single numeric range confuses
money with validity time and still cannot store the old price rows. Keeping
`starts_at` and `ends_at` while relying only on an application pre-check leaves
race conditions and inconsistent overlap definitions.

## Diagnostic Questions

Is the value a bounded label set, a continuous interval, a non-contiguous set of
intervals, or a repeating entity? Does each member need metadata, audit, a
foreign key, or a lifecycle? Will a reviewer need to know bound inclusivity to
understand the answer? Can PostgreSQL reject an impossible row directly? Which
query becomes simpler because the representation is honest? Which query becomes
harder if the type is chosen for fashion instead of workload?

Also ask what the later index signal would be. Array containment and JSONB
containment point toward GIN in indexing phases. Range overlap and exclusion
constraints point toward GiST. That future pointer does not excuse a weak model;
it only tells the learner what performance topic will matter after the
correctness shape is clear.

## Common Pitfalls

Do not put lifecycle-bearing facts inside an array because adding a table feels
heavy. Do not model price history as `numrange`; price is the value, while
validity is the time interval. Do not use two timestamp columns and then define
overlap differently in every service. Do not treat inclusive and exclusive
bounds as decoration. Do not build GIN or GiST indexes in this phase as a way to
avoid explaining the model. A correct answer names both the good-fit use and the
bad-fit redesign it avoids.

## Explain It Back

A strong explanation is concrete: "product tags are an array because the tag
set is small and owned by the product row." Or: "appointment slots are
`tstzrange` because overlap is the invariant and PostgreSQL can compare ranges
directly." Or: "working hours are a multirange because a professional can work
morning and afternoon blocks with a gap." Or: "role grants need a child table
because revocation and audit are separate facts." The answer should make the
tradeoff inspectable without leaning on vague flexibility.

## References and Further Reading

Use `docs/doctrine.md` for the core-first and not-yet doctrine. Use
`docs/constraints-cookbook.md` for the exclusion-constraint pattern. Use
`docs/anti-patterns/arrays_over_child_tables.md` when arrays start hiding child
rows. PostgreSQL documentation for arrays, range types, multiranges, GIN, and
GiST is useful for exact syntax, but Phase 4b keeps implementation tuning as a
future topic.

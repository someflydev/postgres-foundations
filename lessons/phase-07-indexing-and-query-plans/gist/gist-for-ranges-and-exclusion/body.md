# GiST for Ranges and Exclusion

## Problem Framing

GiST matters in the core curriculum because ranges are not scalar values. Scheduling, reservations, maintenance windows, and validity periods often need overlap, containment, and adjacency reasoning. A B-tree can order a start timestamp, but it cannot by itself answer whether two ranges overlap. This lesson revisits Phase 4b ranges with the planner in the room and shows why GiST is the right access method for range operators and exclusion constraints.

The operational standard remains the same: name the operator, prove the plan, and explain maintenance cost. GiST is flexible, but it is not a general upgrade from B-tree. Use it when the operator class and data type need search-tree behavior over intervals, shapes, or extension-defined objects.

Range work is also where modeling and indexing meet directly. If the table stores separate `starts_at` and `ends_at` columns, every query has to reconstruct the interval in its predicate and every constraint has to remember boundary rules. A real range column makes the invariant visible. The index then supports the same representation the application and database constraints use. That is easier to explain, easier to test, and harder to accidentally bypass.

## Minimal Concept Introduction

PostgreSQL range types support operators such as overlap `&&`, contains `@>`, and contained-by `<@`. A GiST index can accelerate those operators because the index stores bounding information that can eliminate ranges that cannot match. Exclusion constraints use the same idea for correctness: prevent two rows from coexisting when a set of operators would conflict.

For scheduling, the important distinction is read performance versus write-time correctness. A query that finds appointments overlapping a candidate window can use a GiST index. An exclusion constraint can prevent double booking. At scale, both need the right operator class and a clear model for boundaries: inclusive start, exclusive end is usually safer than ambiguous endpoints.

## Worked Example

Worked example anchor: appointment-window-range-overlap

A scheduling domain needs to find appointments that overlap a candidate window:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, provider_id, appointment_window
FROM scheduling.appointments
WHERE provider_id = 42
  AND appointment_window && tstzrange('2026-05-14 14:00+00', '2026-05-14 14:30+00', '[)');
```

The operator is `&&`, so the range needs a GiST-backed access path. If the query filters by provider and range together, the design may use an exclusion constraint or a GiST index that includes both dimensions with the right operator classes:

```sql
CREATE INDEX appointments_window_gist_idx
ON scheduling.appointments USING gist (appointment_window);
ANALYZE scheduling.appointments;
```

A correctness-oriented design goes further:

```sql
ALTER TABLE scheduling.appointments
ADD CONSTRAINT appointments_no_overlap
EXCLUDE USING gist (
    provider_id WITH =,
    appointment_window WITH &&
);
```

That exclusion constraint is not just a faster query. It prevents conflicting rows from being inserted. The learner must explain that it also imposes write-time checks and may require careful transaction handling under concurrent booking attempts.

## Diagnostic Questions

Ask which range operator appears in the query. Is the business question overlap, containment, adjacency, or ordering by start time? Ask whether correctness requires an exclusion constraint or whether the index is only for lookup. Ask whether the range boundaries are consistent. Ask whether another predicate, such as `provider_id`, should be part of the design. Ask how many rows are written and whether conflicts are expected during peak scheduling.

Also ask whether the table has enough rows to justify the index. A small appointments table can be faster with a sequential scan. A high-write booking table may need correctness more than read speed, which changes the explanation from tuning to invariant enforcement.

Finally, ask how conflicts should behave in the user workflow. A medical booking system, a room reservation system, and a maintenance window planner may all use range overlap, but they do not all need the same error handling. The index and constraint can reject the bad row, but the product still needs a retry, alternate-slot suggestion, or manual override path.

## Common Pitfalls

The common pitfall is using a B-tree on `starts_at` and `ends_at` and assuming it solves overlap. It may help some range queries, but it does not directly index the range operator. Another pitfall is creating an exclusion constraint without testing concurrent booking behavior. A third is ignoring boundary semantics: `[ ]`, `[)`, `( ]`, and `( )` mean different things. A fourth is using GiST because it sounds advanced when a simple equality or timestamp range predicate would use B-tree more efficiently.

## Explain It Back

A good answer says: "The query asks whether appointment ranges overlap with `&&`, so the access method must support range overlap. A GiST index on the range column can reduce scanned rows. If the requirement is no double booking, an exclusion constraint using GiST encodes the invariant and checks conflicts on write. I verified the lookup with EXPLAIN ANALYZE BUFFERS and would test concurrent inserts before trusting the constraint in production." That connects operator, plan, and correctness.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` and `docs/constraints-cookbook.md` for range indexing and exclusion-constraint design.

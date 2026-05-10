# Declare and prove non-overlap: Exclusion Constraints

## Setup

Use the PostgreSQL Foundations lab and the `scheduling` seed pack at phase 4b.

## Given

Use the lesson topic: EXCLUDE USING gist for professional appointment overlap.

## Task

Create a temporary appointment table with `EXCLUDE USING gist`, insert one slot, attempt an overlapping insert for the same professional, and return evidence that PostgreSQL rejected it with a conflicting key value error.

## Success Criteria

- Name the modeled fact before the PostgreSQL feature.
- Include both a good-fit and bad-fit example when prose is requested.
- Stay inside the Phase 4b boundary.

## Estimated Time

See `exercise.json`.

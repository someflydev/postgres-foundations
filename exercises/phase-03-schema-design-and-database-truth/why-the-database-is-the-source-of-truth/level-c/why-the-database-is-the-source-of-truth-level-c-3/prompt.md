# Why the Database Is the Source of Truth C3

## Setup

Seed the Phase 3 ecommerce pack and run the SQL in your answer file.

## Scenario

Customer contact imports must reject missing identity and duplicate email facts before any application sees them.
## Task

Write the complete schema repair independently, including the constraints that enforce the named invariant. Target table(s): ecommerce.why_the_database_is_the_source_of_truth_c_3.

## Success criteria

- The SQL runs cleanly against the Phase 3 seed pack.
- The resulting table shape and constraints match the reference schema when checked.
- You can name the incident prevented by each database-enforced rule.

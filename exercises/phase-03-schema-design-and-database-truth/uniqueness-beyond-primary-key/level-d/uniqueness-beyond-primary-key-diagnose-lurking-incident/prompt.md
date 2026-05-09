# Uniqueness Beyond Primary Key Incident Review

## Setup

Seed the Phase 3 ecommerce pack and review the schema or fixture named here.

## Scenario

Business identifiers and appointment slots need uniqueness beyond row ids. The incident must be concrete: without this constraint, a bad row could violate a business rule that later workflows trust.

## Task

Diagnose the missing invariant, state the incident that could arise, and propose the ALTER TABLE or CREATE TABLE repair that would prevent it. Include the phrase "without this constraint" in your written diagnosis.

## Success criteria

- Names the missing invariant and the bad row shape.
- Describes the incident in operational terms.
- Proposes PostgreSQL core constraints within the Phase 3 concept boundary.

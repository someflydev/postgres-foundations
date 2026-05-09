# Refactoring Spreadsheet Shape to Relational Incident Review

## Setup

Seed the Phase 3 ecommerce pack and review the schema or fixture named here.

## Scenario

A legacy csv mixes customers, orders, products, and line items in one denormalized sheet. The incident must be concrete: without this constraint, a bad row could violate a business rule that later workflows trust.
Use `seed-data/packs/ecommerce/fixtures/spreadsheet-legacy.csv` and identify customers, orders, products, and order_items before proposing constraints.

## Task

Diagnose the missing invariant, state the incident that could arise, and propose the ALTER TABLE or CREATE TABLE repair that would prevent it. Include the phrase "without this constraint" in your written diagnosis.

## Success criteria

- Names the missing invariant and the bad row shape.
- Describes the incident in operational terms.
- Proposes PostgreSQL core constraints within the Phase 3 concept boundary.

# Refactoring Spreadsheet Shape to Relational B2

## Setup

Seed the Phase 3 ecommerce pack and run the SQL in your answer file.

## Scenario

A legacy csv mixes customers, orders, products, and line items in one denormalized sheet.
Use `seed-data/packs/ecommerce/fixtures/spreadsheet-legacy.csv` as the legacy source shape.

## Task

Complete the ALTER TABLE migration using the starter file as the permissive legacy table. Target table(s): ecommerce.refactoring_spreadsheet_shape_to_relational_b_2_customers, ecommerce.refactoring_spreadsheet_shape_to_relational_b_2_products, ecommerce.refactoring_spreadsheet_shape_to_relational_b_2_orders, ecommerce.refactoring_spreadsheet_shape_to_relational_b_2_items.

## Success criteria

- The SQL runs cleanly against the Phase 3 seed pack.
- The resulting table shape and constraints match the reference schema when checked.
- You can name the incident prevented by each database-enforced rule.

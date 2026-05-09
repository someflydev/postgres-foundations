# Refactoring Spreadsheet Shape to Relational

## Problem Framing

A spreadsheet often mixes customers, orders, products, and line items into one wide sheet. It feels convenient because each row is readable, but it repeats customer names, repeats product descriptions, and hides conflicting facts. Refactoring means finding entities, choosing keys, loading reference tables, and preserving the original import until every fact has a proper relational home.

In Phase 3 the learner already knows how to read joined tables. The new question is what rows should be impossible to store at all. A schema that accepts impossible rows forces every later query to defend itself. The phase therefore treats constraints as executable design notes: they document the rule, reject invalid data, and make later reports less fragile.

## Minimal Concept Introduction

Refactoring Spreadsheet Shape to Relational is taught through ordinary PostgreSQL DDL: CREATE TABLE, ALTER TABLE, NOT NULL, UNIQUE, CHECK, DEFAULT, and FOREIGN KEY. The important habit is naming the invariant before writing syntax. If the invariant cannot be stated in a sentence, the learner is probably copying a pattern instead of designing a rule. PostgreSQL core features are enough here; JSONB, arrays, partitioning, and tuning indexes stay out of scope.

## Worked Example

Start with a permissive table that came from an earlier seed. Inspect the data, repair rows that would violate the intended rule, and then tighten the schema. For example, before adding CHECK (quantity > 0), look for zero or negative quantities and decide whether they are cancelled lines, refunds, or import mistakes. The final ALTER TABLE statement should be small, named, and easy to connect to the business rule.

## Diagnostic Questions

What fact does this column represent? Can the fact be missing, or is NULL hiding a form workflow? Is this value chosen from a controlled list? Can two rows legally share this value? Does a rule compare two columns in the same row? Which existing rows would prevent PostgreSQL from accepting the constraint today?

## Common Pitfalls

Do not use varchar limits as pretend validation. Do not rely on application checks when multiple writers can reach the database. Do not add NOT NULL before backfilling existing rows. Do not normalize only for elegance; normalize to remove repeated facts and update anomalies. Do not denormalize until the operational reason is concrete and the source of truth remains clear.

## Explain It Back

A strong explanation names the incident that becomes impossible. For example: without this constraint, refund processing could insert a negative quantity and inventory reports could increase stock incorrectly. The learner should point to the exact table and column, state the bad row, and describe how PostgreSQL rejects it before the row becomes shared truth.

## References and Further Reading

Use docs/constraints-cookbook.md for local syntax reminders and curriculum/README.md for the phase boundary. PostgreSQL documentation on CREATE TABLE and ALTER TABLE is useful for exact grammar, but the lab keeps the exercises focused on core constraints and reference-table design.

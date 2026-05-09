# Why the Database Is the Source of Truth

## Problem Framing

Application checks are useful, but they are not the final line of defense. Two services, a data repair script, a bulk import, and a psql session can all write to the same tables. If the rule only lives in one application branch, the database will eventually contain rows that another path allowed. PostgreSQL constraints make the rule durable at the place where every writer meets.

In Phase 3 the learner already knows how to read joined tables. The new question is what rows should be impossible to store at all. A schema that accepts impossible rows forces every later query to defend itself. The phase therefore treats constraints as executable design notes: they document the rule, reject invalid data, and make later reports less fragile.

## Minimal Concept Introduction

Why the Database Is the Source of Truth is taught through ordinary PostgreSQL DDL: CREATE TABLE, ALTER TABLE, NOT NULL, UNIQUE, CHECK, DEFAULT, and FOREIGN KEY. The important habit is naming the invariant before writing syntax. If the invariant cannot be stated in a sentence, the learner is probably copying a pattern instead of designing a rule. PostgreSQL core features are enough here; JSONB, arrays, partitioning, and tuning indexes stay out of scope.

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

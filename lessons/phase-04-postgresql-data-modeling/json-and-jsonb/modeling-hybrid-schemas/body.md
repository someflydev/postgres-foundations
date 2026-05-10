# Modeling Hybrid Schemas

## Problem Framing

Modeling Hybrid Schemas belongs in the part of PostgreSQL modeling where a type choice changes the truth a table can carry. The point is not to collect feature names. The point is to ask what fact is being stored, who will compare it, and what bad production row becomes more likely if the type is vague. For hot columns plus cold JSONB as a disciplined hybrid design pattern, a good model makes the common path boring: analysts can filter rows, application code can serialize values, and reviewers can explain the tradeoff without guessing hidden application rules. A bad model makes every later query carry defensive knowledge that should have been visible in the schema.

A good-fit example is a row that records an operational event with a durable meaning. An order was submitted, an appointment starts, a tenant setting was captured, or an external reference was shared with another system. PostgreSQL should preserve that fact in a type that supports the way the fact will be read. A bad-fit example is using hybrid schemas because it looks modern while the real requirement is a normal column, a lookup table, or a simpler scalar value. Phase 4a keeps the focus on modeling and ordinary queries; advanced query decomposition, special indexes, lateral joins, and window functions remain later work.

## Minimal Concept Introduction

The minimal habit is to name the invariant before naming the type. If the fact is an instant, use `timestamptz`; if it is an intentionally local label, document the region and caveats. If the value must be generated outside one central sequence or safely exposed in URLs, a UUID may be appropriate. If the shape is genuinely variable, `jsonb` can hold cold attributes while hot facts stay in columns. PostgreSQL gives precise behavior, but it will not choose the boundary for you.

The hybrid pattern is "hot columns, cold JSONB." Hot columns are constrained, joined, grouped, sorted, or filtered repeatedly. Cold JSONB keys are sparse, provider-specific, or operationally useful without being part of the core invariant. This avoids rewriting table history every time a fulfillment provider adds a minor metadata key, while still preventing stable business facts from disappearing into an unvalidated document.

This lesson uses only Phase 4a tools: scalar columns, UUID defaults from `gen_random_uuid()`, `jsonb` storage and operators, simple joins, basic filters, and straightforward `ALTER TABLE` statements. The learner should still avoid CTEs, window functions, lateral joins, recursive queries, upsert as a topic, and specialized indexes. The absence of those tools is deliberate. It forces the first design question to stay visible: is the stored fact itself shaped correctly?

## Worked Example

Imagine an ecommerce order that needs an internal dense primary key for joins and an externally shareable identifier for support links. The good-fit design keeps `orders.id` as the internal key and adds `orders.external_reference uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE`. That choice avoids leaking row counts while preserving compact internal joins. If the same order also receives operational metadata from fulfillment systems, a `metadata jsonb` column can hold sparse keys such as fraud provider details or campaign tags. Hot facts such as `status`, `total_amount`, and `ordered_at` stay as typed columns because they are filtered, constrained, and reported constantly.

The bad-fit redesign puts the whole order into one document with keys for customer, amount, timestamp, status, and line items. It may look flexible on day one, but it loses foreign keys, makes uniqueness vague, and turns ordinary filters into text extraction. A reviewer should be able to say which attributes are hot columns, which attributes are cold JSONB, and which attributes do not belong in JSONB at all. See [JSONB Everything](../../../../docs/anti-patterns/jsonb_everything.md) for the anti-pattern reference.

## Diagnostic Questions

What is the fact being stored: an instant, a local label, an identifier, or a flexible document fragment? Will users filter or join on it every day? Can PostgreSQL enforce the important rule with a column type, `NOT NULL`, `UNIQUE`, `CHECK`, or a foreign key? Is the value exposed outside the database? Does the shape vary because the domain is truly variable, or because the team has not modeled it yet? What migration would be needed if this choice turns out wrong?

Ask the same questions against the bad-fit design. Which query becomes harder? Which invalid row becomes possible? Which future report will need to know too much about application conventions? If the answer is "every query just extracts a string and hopes," the model is hiding truth.

## Common Pitfalls

Do not use a naive `timestamp` for real-world event time and then tell every client to remember it means UTC. Do not use UUIDs as a default primary-key fashion statement when dense internal keys already serve the workload. Do not put stable, frequently filtered facts inside JSONB because adding a column feels heavy. Do not assume JSONB removes the need for migrations; it often delays the migration until more data is messy. Do not discuss special indexes as the first fix for a weak model. In this phase, explain why a query is awkward before reaching for an index type that has not been introduced.

## Explain It Back

A strong explanation uses concrete rows. For example: "`ordered_at` is `timestamptz` because it records the instant an order was placed; display can convert it to the buyer's locale later." Or: "`external_reference` is a UUID because support links leave the database boundary; the internal `id` remains a dense join key." Or: "`metadata->>'campaign'` is acceptable for occasional attribution, but `status` must be a column because every fulfillment report filters on it." The learner should defend the good fit and name the failure mode of the bad fit.

## References and Further Reading

Use `docs/doctrine.md` for the core-first and not-yet doctrine. Use `docs/anti-patterns/jsonb_everything.md` when the topic touches JSONB misuse. PostgreSQL documentation on date/time types, UUID type, JSON functions, and `pgcrypto` is useful for exact syntax, but this lab keeps the first pass grounded in operational modeling tradeoffs.

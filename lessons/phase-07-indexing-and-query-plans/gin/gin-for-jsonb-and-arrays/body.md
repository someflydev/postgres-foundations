# GIN for JSONB and Arrays

## Problem Framing

GIN is for membership and containment-style questions where one row contains many searchable elements. In this phase, the two important examples are JSONB containment and array membership. The learner's job is not to say "JSONB needs GIN" or "arrays need GIN." The job is to name the operator and prove that the inverted index matches the query. A JSONB extraction predicate, an array length filter, and a containment query are different workloads.

GIN indexes are larger and more expensive to maintain than simple B-tree indexes. They are justified when the read pattern repeatedly asks whether a document or array contains a key, value, or element, and when row counts make sequential scanning too expensive. They are not a substitute for relational modeling. If a field is mandatory, joined, constrained, or used in every transaction, it probably deserves a column or child table rather than a hidden JSONB key.

## Minimal Concept Introduction

GIN stores entries from composite values so PostgreSQL can find rows containing a requested element. For JSONB, the default `jsonb_ops` operator class supports a wider set of operators, including key existence. `jsonb_path_ops` is smaller and often faster for containment with `@>`, but it is narrower. For arrays, GIN can support array membership and overlap operators such as `@>` and `&&`. The operator class and query operator must line up.

This lesson also sets the boundary for full-text search. GIN appears again in Phase 8 for `tsvector`, but this lesson stays with JSONB and arrays. Seeing the same access method in multiple domains should make learners more precise, not less precise.

## Worked Example

Worked example anchor: event-payload-jsonb-containment

An event-heavy operations table stores variable event metadata in `payload`. Incident responders need warning events for one phase:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, occurred_at, payload
FROM events.events
WHERE payload @> '{"phase": 7, "severity": "warning"}'::jsonb
ORDER BY occurred_at DESC
LIMIT 100;
```

The containment operator is the anchor. A targeted GIN index can support it:

```sql
CREATE INDEX events_payload_gin_path_idx
ON events.events USING gin (payload jsonb_path_ops);
ANALYZE events.events;
```

The after plan should show a bitmap index path or another GIN-backed access path with fewer heap pages visited. The answer should explain why `jsonb_path_ops` fits this containment query and what it gives up compared with `jsonb_ops`. If another query uses `payload ? 'severity'` or extracts text with `payload ->> 'severity' = 'warning'`, this index may not be the best match.

For arrays, the shape is similar:

```sql
CREATE INDEX products_tags_gin_idx
ON ecommerce.products USING gin (tags);

SELECT id, sku
FROM ecommerce.products
WHERE tags @> ARRAY['clearance'];
```

That is array membership, not scalar equality. If the tag is actually a normalized category with constraints and joins, the better design may be a child table despite the GIN option.

## Diagnostic Questions

Ask which operator appears in the slow query. Is it `@>`, `?`, `?|`, `&&`, or a text extraction with equality? Ask whether the JSONB keys are optional attributes or disguised core columns. Ask whether the array is a compact attribute list or a many-to-many relationship that needs history, constraints, or ownership. Ask how often rows are updated, because every changed JSONB document or array may touch many GIN entries. Ask whether the index remains selective as common keys grow.

## Common Pitfalls

The first pitfall is creating both `jsonb_ops` and `jsonb_path_ops` indexes without measuring which operators need support. The second is using JSONB because the schema is inconvenient and then trying to repair the design with GIN. The third is missing write cost: a wide, frequently updated JSONB document can make GIN maintenance dominate the benefit. The fourth is assuming a GIN index can satisfy ordering; it usually finds matching rows, while a separate sort or different index handles order.

## Explain It Back

A good answer says: "The query uses JSONB containment with `payload @> ...`, so a GIN index with `jsonb_path_ops` matches the operator and stores a smaller containment-oriented structure than `jsonb_ops`. I verified the before and after plans with buffers. I would not use this as proof that every JSONB predicate is solved; extraction predicates, key-existence checks, and relational invariants need separate decisions." For arrays, say the same thing with array membership and the actual operator.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` and `docs/anti-patterns/jsonb_everything.md` when deciding whether GIN is indexing a good JSONB design or compensating for a weak model.

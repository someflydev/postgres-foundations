# RLS Performance and Indexing

## Problem Framing

RLS policies are predicates PostgreSQL applies to ordinary queries. If the
predicate matches the table's access pattern, RLS can be boring and cheap. If
the predicate hides the indexed column behind functions or joins, every query
may carry avoidable overhead. Multi-tenant systems are especially sensitive
because nearly every dashboard, search, and audit query includes the tenant
boundary. Phase 10 therefore pairs RLS with indexing: security predicates should
be easy for humans to review and easy for the planner to use.

## Minimal Concept Introduction

An RLS predicate such as `tenant_id = current_setting('app.tenant_id')::uuid`
works well with indexes that start with `tenant_id`. A document lookup may use
`(tenant_id, id)`. An audit timeline may use `(tenant_id, occurred_at DESC)`.
The policy is not a separate query clause the learner writes, but it affects
the plan similarly to an added filter. `EXPLAIN` can reveal whether the table
uses an index scan, bitmap scan, or sequential scan after the policy is applied.

## Worked Example

Seed the SaaS corpus and set `app.tenant_id`. Run `EXPLAIN` for a document by
ID or an audit event timeline. The seed includes `documents_tenant_id_id_idx`
and `audit_events_tenant_occurred_idx` because those match the RLS predicate
and common access path. Compare that with a query that casts or transforms the
tenant column itself; the planner has less room to use the index. The repair is
to keep the column raw on one side of the predicate and cast the session value
or parameter to the column type.

## Diagnostic Questions

Does the policy predicate begin with a tenant or ownership key that appears in
common indexes? Are queries also filtering by the same tenant key, or relying
entirely on the hidden policy? Does `EXPLAIN` show rows removed by filter where
an index condition was expected? Is a function call applied to the indexed
column? Are statistics current after seed or bulk load?

## Common Pitfalls

The first pitfall is treating RLS as invisible to performance. It is not.
Another is using expressive but unindexable predicates in the policy. A third
is assuming every table needs the same index. Documents and audit events have
different access paths, so their tenant-leading indexes differ. Finally, do not
use indexes to compensate for vague authorization. A fast bad policy is still a
bad policy.

## Explain It Back

Explain an RLS performance review by naming the protected table, policy
predicate, representative query, supporting index, and observed plan. A good
answer distinguishes security correctness from speed: first prove the boundary,
then prove the common query can use an appropriate path. This habit carries
directly into capstone work, where tenant dashboards must be both isolated and
fast enough for repeated use.

## References and Further Reading

- `docs/rls-playbook.md` for predicate authoring patterns.
- `docs/indexing-playbook-part1.md` and `docs/indexing-playbook-part2.md` for plan review.

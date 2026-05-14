# Plan Debugging Workflow

## Problem Framing

Plan debugging is a disciplined loop. The goal is to move from a vague complaint such as "the query is slow" to a reproducible case, a hypothesis, one controlled change, and a measured result. Without that loop, indexing becomes guesswork. This lesson teaches a workflow learners can repeat during exercises, code review, and production incident analysis.

The workflow is intentionally conservative. Reproduce the query with realistic parameters. Capture `EXPLAIN ANALYZE BUFFERS`. State what the plan is doing and where the mismatch or excess work appears. Hypothesize one cause. Change one thing. Measure again. Keep the change only if it improves the target query without creating unacceptable write, storage, or maintenance cost. Record rollback criteria.

## Minimal Concept Introduction

A good plan investigation has artifacts. The before plan names estimated rows, actual rows, node types, loops, and buffers. The hypothesis predicts what should change. The after plan confirms or rejects that prediction. If the hypothesis is "a partial index should let this query stop after fifty rare rows," the after plan should show the partial index and lower buffers. If the hypothesis is "statistics are wrong," the after plan should show estimates closer to actual rows after `ANALYZE` or `CREATE STATISTICS`.

The workflow also guards against accidental wins. A faster second run may only be warm cache. A new index may help one query and hurt writes. A rewritten predicate may change semantics. A good learner distinguishes those cases.

This is why the workflow asks for a decision, not just a plan screenshot. The learner should finish with a statement that can be reviewed: keep the change, reject it, gather more evidence, or schedule a safer production experiment. Each option should name the evidence that would change the decision. That habit makes plan debugging useful outside the lab, where teams need to explain why a migration or index build is worth the operational risk.

## Worked Example

Worked example anchor: one-change-plan-debugging-loop

A report over event payloads is slow. The team wants to add a GIN index immediately. Start with the actual query:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, occurred_at
FROM events.events
WHERE payload @> '{"severity": "warning"}'::jsonb
  AND occurred_at >= now() - interval '1 day'
ORDER BY occurred_at DESC;
```

Read the plan before changing anything. Suppose it scans the table, removes most rows by filter, and reads many buffers. The hypothesis could be: "The JSONB containment predicate is selective enough that a GIN index on payload will reduce heap work." Make one change:

```sql
CREATE INDEX events_payload_warning_gin_idx
ON events.events USING gin (payload jsonb_path_ops);
ANALYZE events.events;
```

Run the same `EXPLAIN ANALYZE BUFFERS` again. If buffers fall and the GIN path is selective, the hypothesis is supported. If the plan still reads too many rows because almost every event has a severity key, the next hypothesis may be a generated severity column, a time-oriented index, or no index yet. Do not keep piling on indexes without a fresh prediction.

## Diagnostic Questions

Ask what exact symptom is being debugged: latency, buffers, wrong join order, sort spill, lock wait, or write pressure. Ask whether the query and parameters are representative. Ask where the plan first diverges from reality. Ask whether the proposed change targets that point. Ask what secondary costs the change creates. Ask what evidence would make you roll back.

The workflow should also include communication. A pull request should include the before plan, the after plan, the index definition or statistics change, and the reason the new maintenance cost is acceptable. If the change is temporary for an incident, the cleanup date should be explicit.

When the answer is \"not yet,\" it should still be specific. \"Not yet\" may mean the table is too small, the data distribution in staging is not representative, the proposed predicate is not the production predicate, or the write cost is unknown. A vague refusal is not useful. A precise refusal gives the team the next measurement to collect.

## Common Pitfalls

The first pitfall is changing several things at once: adding an index, rewriting the query, and running `ANALYZE`, then claiming victory without knowing which change mattered. The second is benchmarking on a toy dataset. The third is ignoring writes and vacuum after a read improvement. The fourth is relying on a single timing run. The fifth is using production-only observations without creating a safe reproduction path.

## Explain It Back

A strong explanation says: "I reproduced the slow query, captured `EXPLAIN ANALYZE BUFFERS`, and found the large buffer cost at the JSONB filter. I hypothesize that containment selectivity justifies a GIN index. I changed only that, ran ANALYZE, measured again, and compared buffers, actual rows, and node types. If write cost or low scan count later outweighs the benefit, I will drop the index." The important verbs are hypothesize, measure, and decide.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` for the workflow checklist and `docs/observability-intro.md` for connecting query plans to operational signals.

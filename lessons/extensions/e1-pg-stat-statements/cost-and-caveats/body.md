# Cost and Caveats

## Problem Framing

This extension lesson is about overhead, normalization edge cases, dynamic SQL, IN lists, and JSONB path expressions. The extension track keeps the core-first doctrine explicit: start with the PostgreSQL feature already available, name the workload signal that is missing, and only then decide whether pg_stat_statements earns its operational cost. A learner should leave this lesson able to say what the extension adds, what remains good enough without it, and what evidence would justify enabling it in a production cluster. The decision is not simply a syntax preference. It touches query plans, statistics, write overhead, backup and restore expectations, replication behavior, upgrade planning, and managed-service portability.

## Minimal Concept Introduction

For Cost and Caveats, the first concept is scope. A row is a normalized statement aggregate, not a trace of one request. Literals are folded, query text can be truncated, and highly dynamic SQL may fragment evidence. The second concept is measurement. Do not ask whether the extension is popular; ask whether the workload has repeated symptoms that core PostgreSQL cannot answer cleanly enough. The third concept is reversibility. A good rollout can be explained with a narrow SQL change, a baseline query, an expected improvement, and a rollback plan. In this repository, extension mastery means using the extension as evidence or capability while keeping the surrounding system understandable to an operator who inherits it later.

## Worked Example

A useful drill starts from a concrete question, then writes the smallest SQL that exposes the evidence. The query below is intentionally compact so the operator can paste it into a runbook, compare it before and after a change, and explain why each column matters.

```sql
SELECT queryid, calls, round(total_exec_time::numeric, 2) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       shared_blks_read, shared_blks_hit, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

Read the output as a decision aid. Sort order tells you the question being asked. A total-time ranking asks where the database spent time overall. A similarity ranking asks which records are plausible matches for user input. Neither ranking is the final answer by itself. It should lead to an EXPLAIN plan, a threshold discussion, an index review, a product decision, or a not-yet recommendation.

## Diagnostic Questions

What user-visible symptom caused this investigation? Which PostgreSQL core feature handles the requirement today, and where does it fail? What metric or result set would change if pg_stat_statements is the right tool? How often is the underlying data written, and who pays the write or collection overhead? Does the managed service support the required version and settings without superuser-only work? What evidence would prove that the change improved the workload instead of only moving cost elsewhere?

## Common Pitfalls

The first pitfall is enabling an extension because it appears in a recipe. That skips the workload signal and makes later incidents harder to explain. The second pitfall is treating one successful query as a contract. Operators need baselines, representative input, and enough volume to see planner behavior. The third pitfall is ignoring portability. Some extensions are broadly available; others vary by provider or need local operations knowledge. The fourth pitfall is forgetting the core alternative. If a btree prefix lookup, a generated column, core full-text search, or a better EXPLAIN workflow solves the problem, the right answer may be not yet.

## Explain It Back

Explain this lesson as a production change request. Name the symptom, the core PostgreSQL behavior that is still useful, the missing capability, the extension setting or SQL you would add, and the verification query you would run after deploy. Then name one case where you would refuse the extension for now. A strong answer is operationally specific: it includes a baseline, a threshold, an owner for maintenance, and a plan for what to do if the result is ambiguous.

## References and Further Reading

Use `docs/doctrine.md` for extension posture, `docs/search-playbook.md` for search boundaries, and the extension-track module docs for this lesson. Pair pg_stat_statements work with the Phase 7 indexing playbooks and the administration monitoring playbook when the change affects production operations.

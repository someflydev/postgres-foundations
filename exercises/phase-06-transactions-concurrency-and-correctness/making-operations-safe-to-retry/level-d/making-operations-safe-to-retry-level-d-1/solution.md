# Reference Solution

Runs against the harness introduced in PROMPT_19.

## Expected Interleaving

```sql
-- session 1
BEGIN;
-- perform the first read or lock shown in the prompt
```

```sql
-- session 2
BEGIN;
-- perform the competing read or lock before session 1 commits
```

```sql
-- session 1
-- apply the write, commit, and record whether session 2 blocked or later failed
COMMIT;
```

```sql
-- session 2
-- continue after the wait or retry boundary and capture the final observation
COMMIT;
```

## Outcome

The unsafe interleaving lets both sessions make a decision from incomplete information. The repair either serializes the decision with a row lock, uses an atomic conditional write, makes PostgreSQL abort a non-serializable history, or enforces a durable uniqueness/range invariant. The final answer should include the observed rows, waits, errors, and retry point.

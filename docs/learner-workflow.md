# Learner Workflow

PostgreSQL Foundations uses a small repeatable loop:

1. Pick one active exercise from the phase README.
2. Load the seed pack when needed.
3. Run the exercise prompt.
4. Write an answer in `tmp/answers/<exercise-id>.sql`.
5. Check the answer.
6. Record the attempt and move on.

## Running an exercise

Use `pgfound exercise run` to print the prompt, show the seed pack, and open
`psql`:

```sh
uv run pgfound exercise run first-select-write-query --auto-seed
```

The runner sets the exercise search path for the interactive session, so a
single-schema exercise can use unqualified table names. The prompt still shows
the seed pack and phase so the loaded data is explicit.

When iterating on a known problem, skip the prompt:

```sh
uv run pgfound exercise run first-select-write-query --no-prompt
```

## Checking an answer

The default answer path is `tmp/answers/<exercise-id>.sql`:

```sh
uv run pgfound exercise run first-select-write-query --check
```

To check a different file:

```sh
uv run pgfound exercise run first-select-write-query --check --answer tmp/scratch.sql
```

Each non-dry-run session writes a progress record under
`tmp/progress/exercises/<exercise-id>.json`. These files are local learner
state and remain ignored by git.

## Progress

Progress files use this shape:

```json
{
  "exercise_id": "first-select-write-query",
  "attempts": [
    {
      "started_at": "2026-04-23T14:00:00-07:00",
      "completed_at": "2026-04-23T14:22:00-07:00",
      "self_assessment": "correct",
      "check_result": "correct",
      "notes": ""
    }
  ]
}
```

Show a minimal summary:

```sh
uv run pgfound progress show
```

## Reset and Snapshot

Before experimenting with schema changes, take a snapshot:

```sh
uv run pgfound lab snapshot before-constraints
```

Reset one domain to its latest available seed phase:

```sh
uv run pgfound lab reset-domain ecommerce
```

Restore a snapshot:

```sh
uv run pgfound lab restore before-constraints
```

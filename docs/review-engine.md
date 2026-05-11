# Review Engine

The review engine turns learner artifacts into structured review reports. It
runs mechanical checks, emits findings and signals, scores rubric dimensions
where a signal mapping exists, and queues the remaining dimensions for human
review.

Exercise review:

```bash
uv run pgfound exercise review first-select-write-query --answer tmp/answers/first-select-write-query.sql --auto
```

The command loads the exercise seed pack, runs the existing `exercise --check`
comparator, scores the exercise rubric, and writes Markdown and JSON reports
under `tmp/reviews/<exercise-id>/`. Use `--full` to add
`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` plan comparison when a live lab is
available.

Capstone review:

```bash
uv run pgfound capstone evaluate 01-multi-tenant-saas-crm --path capstones/01-multi-tenant-saas-crm/reference
```

Prompt 27 implements deterministic artifact checks for schema, indexes, RLS,
critical queries, operational runbook, and writeup sections. Use `--full` to run
schema/index/RLS SQL and reference-vs-learner critical query files inside a
rollback against the sandbox database URL. Set `PGFOUND_SANDBOX_DB_URL` or start
the sandbox profile on port 55434.

Full capstone evaluation also renders provider-neutral reviewer prompts under
`tmp/reviews/capstone/<id>/<timestamp>/prompts/` and a concatenated
`prompt-bundle.md` beside them. The bundle includes full-capstone,
operational-runbook, writeup, and extension-posture review prompts, all seeded
with learner artifacts, reference artifacts, engine findings, and rubric
metadata. The local CLI does not call an LLM; a coach can send the bundle to an
external provider and keep the deterministic Markdown/JSON reports as the
source of engine evidence.

Reports begin with a weighted dimension table, then group findings by severity,
and include a manual-review queue for dimensions that were not auto-scored.

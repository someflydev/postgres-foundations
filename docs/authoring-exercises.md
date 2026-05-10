# Exercise Authoring

Exercises are the flight-school part of PostgreSQL Foundations. A lesson may
explain a concept, but an exercise asks the learner to recognize it, produce
with support, produce independently, or critique and repair a broken artifact.
Every exercise belongs to exactly one lesson and exactly one scaffolding level.

## Directory Layout

Author exercises under the root `exercises/` tree, not under `curriculum/`:

```text
exercises/
  phase-00-reality-before-syntax/
    <lesson-slug>/
      level-a/<exercise-slug>/
        exercise.json
        prompt.md
        starter.sql
        solution.md
        solution.sql
```

The phase directory mirrors `lessons/`. The lesson directory is the parent
lesson slug. `exercise.json` is metadata, `prompt.md` is what the learner sees,
`starter.sql` is optional starter material, `solution.md` is the private
reference explanation, and `solution.sql` is required only when an active
`query`, `schema`, or `lab` exercise has an executable SQL answer.

## Pick the Level

Level A is recognition. Use it for multiple-choice, short identification, or
small inspection prompts. `expected_output_shape` is usually
`prose_explanation` or `scalar`; `kind` is typically `critique` or `query`.
Hints are allowed, time target is 5-10 minutes, and oral defense is optional.

Level B is controlled production. Use it when the learner should write a
bounded query, schema object, or lab step with starter SQL and hints. The common
output shapes are `rowset` and `schema_object`. Time target is 10-25 minutes and
2-4 hints are appropriate.

Level C is independent production. Use it after a learner has seen a similar
pattern and should now produce without hints. `hints` must be absent or empty.
`oral_defense_prompts` are required for active content, with at least two
questions. Time target is 20-45 minutes.

Level D is critique and repair. The learner receives a broken schema, broken
query, or wrong-but-passing answer, then diagnoses, fixes, and explains the
defect. `kind` must be `critique` or `debug`. Hints are not allowed. Active
Level D exercises require at least three oral defense prompts. Time target is
20-60 minutes.

## Scaffold

Start from the lesson path under `lessons/`:

```sh
uv run pgfound content scaffold exercise \
  --lesson phase-07/index-fundamentals/btree-composite-vs-single-column \
  --level c \
  --slug analyze-composite-plan \
  --kind query \
  --title "Analyze a composite B-tree plan"
```

The scaffolder verifies the lesson exists, then creates
`exercises/<phase>/<lesson-slug>/level-<level>/<slug>/`. It seeds
`allowed_concepts` from the parent lesson and prior lesson concepts, and seeds
`not_yet_allowed_concepts` from the parent lesson boundary plus later curriculum
concepts. It refuses to overwrite existing authored files.

## Write `prompt.md`

Every learner prompt uses this order:

1. Setup: lab, seed pack, and how to enter the lab.
2. Given: facts the learner can rely on, such as schema and data.
3. Task: exactly what the learner must produce.
4. Allowed concepts: echoed from `allowed_concepts`.
5. Not yet allowed: echoed from `not_yet_allowed_concepts`; rubrics should
   penalize use of these concepts.
6. Success criteria: verbatim from `success_criteria`.
7. Oral defense: C and D only, echoed from `oral_defense_prompts`.
8. Estimated time.

Keep the prompt operational. Do not hide new requirements in prose outside the
success criteria, and do not include private solution reasoning.

## Write Solutions

Use `solution.md` for the reference answer and annotated reasoning. It is never
shown to learners automatically. When the answer can be executed as SQL, add
`solution.sql`. Active `query`, `schema`, and `lab` exercises must have that
file. `starter.sql` should contain only scaffolding that the learner is allowed
to see; omit it for modeling-only exercises when SQL starter text would confuse
the task.

For executable row-set exercises, set `output_comparison` when row order or
duplicate rows matter:

- `unordered` is the default. It compares returned rows as an unordered set and
  ignores duplicate multiplicity.
- `multiset` ignores row order but preserves duplicate multiplicity.
- `ordered` requires the same rows in the same order, so the reference solution
  should include an `ORDER BY` when deterministic ordering is intended. Use it
  for window-function drills, top-N reports, running totals, and any answer
  where ordering is part of the skill being assessed.

Learners can run `pgfound exercise run <exercise-id> --check --timing` to see
the reference-query and answer-query execution times. Treat this as a soft
signal for discussion, not a grading threshold; performance as a primary topic
arrives in the indexing and query-plan phase.

Multi-statement `solution.sql` files are allowed for setup or inspection, but
the checker compares only the last statement that returns rows. Author the last
`SELECT` as the learner-visible answer shape.

Phase 0 is a paper-modeling phase. Active Phase 0 exercises with
`kind: modeling` use markdown prompts, `solution.md`, and, when needed,
`starter.md` instead of SQL starter or solution files. The validator implements
this as a per-phase exercise override: Phase 0 marks modeling exercises as
having optional `solution.sql`, while later executable exercise kinds still
require a SQL solution. The same override allows Level D Phase 0 critique and
repair work to remain `kind: modeling`, because the artifact being repaired is a
paper model rather than SQL. The override shape is documented by
`content-schemas/phase-exercise-overrides.schema.json`.

## Rubrics

Default rubrics live in `rubrics/default/`:

- `query-correctness`
- `schema-design`
- `paper-modeling`
- `indexing-reasoning`
- `concurrency-reasoning`
- `critique-and-repair`

Set `rubric_id` to one of these IDs when it fits. Use a custom rubric only when
the default dimensions would cause reviewers to score different competencies
than the exercise is actually testing.

## Validate, Lint, Activate

Run validation before review:

```sh
uv run pgfound content validate
```

Validation checks the schema, lesson references, rubric references, level
directory consistency, C/D oral defense minimums, hint rules, concept-boundary
overlap, parent lesson boundaries, and required `solution.sql` for active SQL
exercises.

Run lint for author-facing warnings:

```sh
uv run pgfound content lint
```

Forbidden-concept lint scans each `solution.sql` for best-effort SQL patterns
when the matching concept is listed in `not_yet_allowed_concepts`. Known
patterns include `window_function` via `OVER (...)`, `cte` via `WITH name AS`,
`recursive_cte` via `WITH RECURSIVE`, `lateral_join` via `LATERAL`,
`view` and `materialized_view` via `CREATE VIEW` forms, `upsert` via
`ON CONFLICT`, `jsonb` via `jsonb` casts or type names, and `array` via
`ARRAY[...]` or `unnest(...)`. A warning means the author must justify the
boundary crossing or rewrite the solution.

Only set `status` to `active` after placeholders are resolved, the prompt
matches metadata, the reference solution is reviewable, and validation passes.

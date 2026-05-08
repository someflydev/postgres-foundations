# Content Authoring

PostgreSQL Foundations content is JSON-first. YAML files with `.yml` or
`.yaml` are accepted by the validator for authoring ergonomics, but JSON is the
default format for reviewable content.

## Locations

Author real content in these directories:

- `lessons/**/lesson.json` for lessons.
- `exercises/**/exercise.json` for exercises.
- `rubrics/**/*.json` for rubrics.
- `scenarios/**/*.json` for scenarios.
- `capstones/**/*.json` for capstones.

Schema examples live in `content-schemas/examples/`. They are validator fixtures
and authoring references, not curriculum.

## Required Fields

Lesson files must fill `id`, `title`, exactly one of `phase` or `module_id`,
`capability_layer`, `summary`, `learning_objectives`, `body_path`,
`estimated_time_minutes`, and `status`. Optional lesson fields include
`prerequisites`, `concepts_introduced`, `concepts_not_yet_allowed`,
`worked_example_path`, exercise ID arrays, `reflection_prompts`, `references`,
and `tags`.

## Lesson Directory Layout

Lessons are authored as small directories rather than a single JSON file:

```text
lessons/
  phase-00-reality-before-syntax/
    <cluster-slug>/
      <lesson-slug>/
        lesson.json
        body.md
        worked-example.md
        figures/
```

Phase directories use the zero-padded phase number plus the phase slug from
`curriculum/map.json`, for example `phase-07-indexing-and-query-plans`.
`body_path` and `worked_example_path` in `lesson.json` resolve relative to the
lesson directory.

## Lesson Body Structure

Every `body.md` uses these seven sections, in this order:

1. Problem Framing
2. Minimal Concept Introduction
3. Worked Example
4. Diagnostic Questions
5. Common Pitfalls
6. Explain It Back
7. References and Further Reading

This structure keeps the five parallel loops embedded in authoring practice:
`body.md` drives the lesson loop; exercises drive the lab, debug, and design
loops; rubrics drive the review loop. A lesson should frame a concrete problem,
introduce only the concepts it owns, show a short lab-grounded example, ask
diagnostic questions, name pitfalls, require the learner to explain the idea
back, and point to titled references.

Exercise files must fill `id`, `title`, `lesson_id`, `scaffolding_level`,
`kind`, `schema_scope`, `expected_output_shape`, `success_criteria`,
`time_target_minutes`, `solution_path`, and `status`. Exercises may also fill
`allowed_concepts`, `not_yet_allowed_concepts`, `dataset`, `rubric_id`,
`starter_path`, `hints`, `oral_defense_prompts`, and `tags`. Level C and D
exercises must include `oral_defense_prompts`.

Exercises are authored as directories under root `exercises/`; see
`docs/authoring-exercises.md` for the level conventions, `prompt.md` structure,
scaffold command, solution files, and forbidden-concept lint.

Rubric files must fill `id`, `title`, `applies_to`, `dimensions`, and
`pass_threshold`. Each dimension must have `name`, `weight`, and `levels` with
scores `0`, `1`, `2`, `3`, and `4`. `notes` is optional.

Scenario files must fill `id`, `title`, `industry`, `narrative_path`, `context`,
`data_shapes`, `workload_patterns`, and `expected_decision_outputs`. The
`context` object must include `team_size`, `scale_signals`, `tenancy_model`,
`portability_requirements`, and `operational_tolerance`. Suggested lesson,
exercise, and capstone references plus `tags` are optional.

Capstone files must fill `id`, `title`, `industry`, `summary`,
`phases_required`, `deliverables`, `critical_queries`, `security_posture`,
`operational_notes`, `review_rubric_id`, and `tags`. Each deliverable needs
`name`, `kind`, and `path`.

## Validation

Validate the current authored content tree:

```sh
uv run pgfound content validate
```

Validate the schema examples too:

```sh
uv run pgfound content validate --include-examples
```

Validate one file or subset:

```sh
uv run pgfound content validate --paths 'lessons/**/lesson.json'
uv run pgfound content validate --paths lessons/phase-01-sql-literacy-basics/reading-rows/first-select/lesson.json
```

Use `--strict` when warnings should fail the command:

```sh
uv run pgfound content validate --strict
```

## Cross-Checks

The validator enforces schema shape and these repository-level checks:

- Lessons must have exactly one of `phase` or `module_id`.
- Lesson `body_path` must resolve relative to the lesson directory.
- Active lesson metadata and body files must not contain `__REPLACE_ME__`
  placeholders.
- Active lessons warn when no exercise references their lesson ID.
- Lesson `phase` must match the enclosing `phase-NN-...` directory.
- Lesson `concepts_not_yet_allowed` must not overlap `concepts_introduced`.
- Exercise `lesson_id` must reference an existing lesson in the validation set.
- Exercise `rubric_id`, when present, must reference an existing rubric in the
  validation set.
- Exercise `exercise.json` must live under a matching `level-a` through
  `level-d` directory.
- Level C and D exercises must not include hints, and active Level C/D
  exercises must meet oral-defense minimums.
- Active `query`, `schema`, and `lab` exercises must include `solution.sql`.
- Exercise `not_yet_allowed_concepts` must include every concept listed in the
  parent lesson's `concepts_not_yet_allowed`.
- Rubric dimension weights must sum to `1.0` within `0.000001`.
- Scenario `data_shapes` and `workload_patterns` are checked against
  decision-engine catalogs when those catalogs exist. Missing catalogs produce
  warnings until the decision-engine prompt creates them.

## Lesson Lint

`pgfound content lint` runs authoring checks that are useful before publishing
but are not required for draft validation:

```sh
uv run pgfound content lint
uv run pgfound content lint --strict
```

Lint checks active lesson bodies for at least 400 words, all seven required
sections, titled links instead of bare URLs, and no TODO/TBD/XXX tokens. Without
`--strict`, lint prints warnings and exits 0.

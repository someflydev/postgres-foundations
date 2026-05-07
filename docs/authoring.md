# Content Authoring

PostgreSQL Foundations content is JSON-first. YAML files with `.yml` or
`.yaml` are accepted by the validator for authoring ergonomics, but JSON is the
default format for reviewable content.

## Locations

Author real content in these directories:

- `curriculum/lessons/**/*.json` for lessons.
- `curriculum/exercises/**/*.json` for exercises.
- `curriculum/rubrics/**/*.json` for rubrics.
- `curriculum/scenarios/**/*.json` for scenarios.
- `curriculum/capstones/**/*.json` for capstones.

Schema examples live in `content-schemas/examples/`. They are validator fixtures
and authoring references, not curriculum.

## Required Fields

Lesson files must fill `id`, `title`, exactly one of `phase` or `module_id`,
`capability_layer`, `summary`, `learning_objectives`, `body_path`,
`estimated_time_minutes`, and `status`. Optional lesson fields include
`prerequisites`, `concepts_introduced`, `concepts_not_yet_allowed`,
`worked_example_path`, exercise ID arrays, `reflection_prompts`, `references`,
and `tags`.

Exercise files must fill `id`, `title`, `lesson_id`, `scaffolding_level`,
`kind`, `schema_scope`, `expected_output_shape`, `success_criteria`,
`time_target_minutes`, `solution_path`, and `status`. Exercises may also fill
`allowed_concepts`, `not_yet_allowed_concepts`, `dataset`, `rubric_id`,
`starter_path`, `hints`, `oral_defense_prompts`, and `tags`. Level C and D
exercises must include `oral_defense_prompts`.

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
uv run pgfound content validate --paths 'curriculum/lessons/**/*.json'
uv run pgfound content validate --paths curriculum/lessons/phase0/select.json
```

Use `--strict` when warnings should fail the command:

```sh
uv run pgfound content validate --strict
```

## Cross-Checks

The validator enforces schema shape and these repository-level checks:

- Lessons must have exactly one of `phase` or `module_id`.
- Exercise `lesson_id` must reference an existing lesson in the validation set.
- Exercise `rubric_id`, when present, must reference an existing rubric in the
  validation set.
- Exercise `not_yet_allowed_concepts` must include every concept listed in the
  parent lesson's `concepts_not_yet_allowed`.
- Rubric dimension weights must sum to `1.0` within `0.000001`.
- Scenario `data_shapes` and `workload_patterns` are checked against
  decision-engine catalogs when those catalogs exist. Missing catalogs produce
  warnings until the decision-engine prompt creates them.

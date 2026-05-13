# Decision Rules

Rules are small, auditable JSON files that connect factual intake signals to
catalog-backed recommendations. They are deliberately conservative: prefer
`candidate_later`, `not_enough_evidence`, or `avoid_for_now` when the intake
does not prove that more operating surface is justified.

## Shape

Each rule has `id`, `title`, `status`, `when`, and `then`. The `when` block may
contain `if_all`, `if_any`, and `if_not`; each list contains one-key predicates.
The `then` array may produce multiple recommendations. Every recommendation
must cite a catalog `target_slug`, carry `why_now`, `why_not_yet`, and
`triggers_for_next_stage`, and use confidence in the range `0.4` to `0.95`.

Anti-pattern files use `kind: anti_pattern_warning` and `verdict:
avoid_for_now`. Rules that only need more facts may use `request_more_information`
with `followup_questions`, though the initial pack primarily emits catalog
recommendations.

## Predicate Vocabulary

- `industry_is: <slug>` / `industry_in: [slugs]`
- `data_shape_present: <slug>` / `data_shape_any_of: [slugs]` /
  `data_shape_all_of: [slugs]`
- `workload_pattern_present: <slug>` / `workload_pattern_any_of: [slugs]`
- `scale_signal_gte: { key, value }` / `scale_signal_lt: { key, value }`
- `tenancy_model_is: <slug>` / `tenancy_model_in: [slugs]`
- `security_constraint_present: <slug>`
- `portability_constraint_present: <slug>`
- `operational_tolerance_is: low|medium|high`
- `existing_topology_is: <slug>`
- `migration_need: <field>`
- `free_form_notes_contains: <substring>`
- `explicit_bias_for_contains: <slug>`
- `explicit_bias_against_contains: <slug>`

`scale_signal_gte` and `scale_signal_lt` accept the intake scale fields plus
`largest_table_rows`, which is derived from `row_counts_largest_tables`.

## Authoring Guidance

Use catalog slugs exactly as authored under `decision-engine/catalogs/`. Keep
rules narrow enough that a reviewer can explain why they triggered. A rule that
recommends an extension should usually also name what would make the extension
premature. For example, a pgvector rule should mention lexical baselines,
embedding refresh, permissions, and recall tests; a Citus rule should mention a
stable distribution key and cluster restore drills.

Run `uv run pgfound decision rules lint` before committing rule changes. Use
`uv run pgfound decision run <intake> --rules '<glob>' --explain <target_slug>`
to inspect one rule or one rule family in isolation.

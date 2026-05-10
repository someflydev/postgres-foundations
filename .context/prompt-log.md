# Prompt Log

Completed:

- PROMPT_01: repository scaffolding, Python/uv environment, top-level layout.
- PROMPT_02: doctrine, architecture overview, LLM usage, repo layout, and ADR
  infrastructure.
- PROMPT_03: Docker Compose PostgreSQL lab environment, init SQL, sandbox
  profile, lab guide, Makefile lab targets, and compose-file tests.
- PROMPT_04: `pgfound` package layout, Click command surface, config/path
  helpers, Docker lab wrappers, content loader placeholders, CLI docs, and
  hermetic CLI tests.
- PROMPT_05: draft 2020-12 content schemas, schema examples, real
  `pgfound content validate`, authoring docs, and validator tests.
- PROMPT_06: canonical curriculum map in JSON and Markdown, capability-layer
  and reusable-domain docs, shared glossary, curriculum schema, validator
  integration, and tests.
- PROMPT_07: lesson authoring directories, lesson templates, scaffold command,
  lesson validation cross-checks, authoring lint, docs, and tests.
- PROMPT_08: exercise authoring directories, scaffold command, level-specific
  validation, forbidden-concept SQL lint, default rubrics, docs, and tests.
- PROMPT_09: reusable teaching domain packs, domain conventions, seed loader
  CLI, manifest validation, dry-run tests, and deterministic generators.
- PROMPT_10: full Phase 0 reality-before-syntax paper modeling corpus, 10
  active lessons, 40 active modeling exercises, paper-modeling rubric,
  per-phase validator overrides, authoring docs, domain README notes, pointer
  tables, and corpus tests.
- PROMPT_11: full Phase 1 SQL literacy basics corpus, 10 active lessons, 70
  active SQL exercises, Phase 1 pointer tables, `pgfound exercise run`, dry-run
  and answer-check support, and Phase 1 corpus/runner tests.
- PROMPT_12: full Phase 2 relational joins and aggregation corpus, 8 active
  lessons, 56 active SQL exercises, Phase 2 seed extensions, row-set output
  comparison modes, pointer tables, and Phase 2 corpus tests.
- PROMPT_13: full Phase 3 schema design and database-truth corpus, 12 active
  lessons, 68 schema/critique exercises, Phase 3 seed constraints for
  ecommerce/scheduling/SaaS, spreadsheet legacy fixture, schema-object answer
  checking, constraints cookbook, and Phase 3 corpus tests.
- PROMPT_14: seed doctor, per-exercise search_path metadata, canonical
  tmp/progress exercise attempts, lab reset/snapshot/restore helpers, exercise
  runner QoL flags, learner workflow docs, and seed/progress tests.
- PROMPT_15: Phase 4a PostgreSQL data modeling corpus for timestamps/time
  zones, UUIDs, and JSON/JSONB; 9 active lessons, 63 active exercises, Phase
  4a seed extensions for ecommerce/scheduling/SaaS, JSONB anti-pattern docs,
  JSON-aware row comparison, and Phase 4a corpus tests.
- PROMPT_16: Phase 4b PostgreSQL data modeling corpus for arrays, ranges, and
  multiranges; 10 active lessons, 70 active exercises, Phase 4b seed
  extensions for ecommerce/scheduling/event-heavy ops, arrays-over-child-tables
  anti-pattern docs, exclusion constraints cookbook coverage, array/range
  comparison normalization, and Phase 4b corpus tests.

Next expected prompt:

- PROMPT_17: Phase 5 expressive querying.

Notes:

- Do not run PROMPT_17 unless the user explicitly asks.

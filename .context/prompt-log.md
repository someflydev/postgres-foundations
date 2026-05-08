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

Next expected prompt:

- PROMPT_12: Phase 2 relational joins and aggregation.

Notes:

- Do not run PROMPT_12 unless the user explicitly asks.
- PROMPT_12 should verify its cluster list against `curriculum/map.json`
  before authoring because the prompt text's sample cluster names do not match
  the current map exactly.

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
- PROMPT_17: Phase 5 expressive querying corpus for CTEs, recursive CTEs,
  window functions, lateral joins, upserts, EXISTS/NOT EXISTS, views,
  materialized views, and synthesis; 12 active lessons, 96 active exercises,
  Phase 5 seed extensions for ecommerce/scheduling/SaaS/event-heavy ops,
  expressive SQL style guidance, glossary additions, ordered-output authoring
  guidance, exercise-runner `--timing`, and Phase 5 corpus tests.
- PROMPT_18: Phase 6 transactions, concurrency, and correctness corpus for
  transactions, MVCC, isolation levels, lost updates, write skew, phantom
  range checks, row locks, deadlocks, and idempotency; 12 active lessons, 96
  active exercises, Phase 6 ecommerce/scheduling seed extensions, a small
  `bank` transfer mini-domain, multi-session exercise metadata and scaffolding,
  concurrency playbook docs, glossary additions, and Phase 6 corpus tests.
- PROMPT_19: Multi-session concurrency lab harness, `pgfound lab concurrency`
  commands, scenario library, `multi_session_trace` check integration, harness
  docs, and scenario validation tests.
- PROMPT_20: Phase 7a indexing fundamentals corpus for scans, EXPLAIN basics,
  B-tree, composite indexes, covering indexes, and index costs; 8 active
  lessons, 64 active exercises, generated ecommerce/scheduling volume seeds,
  `pgfound lab explain`, indexing and observability docs, glossary additions,
  and Phase 7a corpus tests.
- PROMPT_21: Phase 7b advanced indexing corpus for partial indexes,
  expression indexes, GIN, GiST, BRIN, deeper EXPLAIN, estimated-vs-actual
  debugging, and extended statistics; 10 active lessons, 80 exercises, Phase
  7b ecommerce/event seed extensions, indexing playbook part 2, unused and
  redundant index anti-pattern docs, and fixture-based explain diff tests.

- PROMPT_22: Phase 8 full-text search in PostgreSQL core; 10 active lessons,
  80 exercises, a 5000-row `document_search` FTS corpus, ecommerce product
  search vectors, `unaccent`, pg_trgm/pgvector forward pointers, and
  `docs/search-playbook.md`.
- PROMPT_23: Phase 9 partitioning and large-table operations; 10 active
  lessons, 80 exercises, `events.event_log_partitioned` monthly range
  partitions with a detached cold partition example, `ecommerce.orders_partitioned`
  quarterly comparison table, deterministic Phase 9 partition manifest
  generator, `docs/partitioning-playbook.md`, partition-too-early anti-pattern,
  partitioned-index guidance, and Phase 9 corpus/seed tests.
- PROMPT_24: Phase 10 roles, RLS, logical replication, and FDW; 12 active
  lessons, 96 exercises, SaaS document/audit RLS seed policies,
  modernization loopback `postgres_fdw` seed bridge, a replication Docker
  profile with `pg-replica`, RLS and logical replication playbooks, lab docs,
  glossary additions, and Phase 10 corpus/RLS policy tests.
- PROMPT_25: Capstones 1 and 2 for multi-tenant SaaS CRM and scheduling
  availability; capstone starter/reference layouts, composed capstone rubrics,
  `pgfound capstone start|evaluate`, scheduling concurrency scenario, and
  capstone corpus/CLI tests.
- PROMPT_26: Capstones 3 and 4 for event-heavy operations and modernization
  bridge; capstone starter/reference layouts, retention and FDW wiring
  artifacts, extension-posture and operational-reasoning rubric dimensions,
  backported capstone rubric composition, a stale materialized-view FDW
  concurrency scenario, a Phase 10 critique exercise, capstones README, and
  capstone corpus tests.
- PROMPT_27: Mechanical review engine and rubric signal system; exercise and
  capstone review commands, Markdown/JSON report writers, plan diff helpers,
  writeup lint, schema/artifact runners, rubric `signals`, capstone
  `critical_queries_path` and `writeup_required_sections`, and review-engine
  docs/tests.
- PROMPT_28: Interview simulator scaffolding; interview scenario loader,
  session state machine, transcript parser/persistence, stubbed LLM prompt
  logging, deterministic interview rubric evaluation, `pgfound interview
  start|review`, interview rubrics, six interview scenarios, dedicated
  interview scenario schema, prompt templates, docs, and tests.
- PROMPT_29: Training-side LLM prompt templates for coaching, critique,
  remediation, and the shared trainer persona; Markdown/YAML front-matter
  template format; Jinja2-backed `pgfound llm list|render`; full exercise
  review prompt artifacts; full capstone schema/index prompt artifacts; LLM
  integration docs; and template render/completeness tests.
- PROMPT_30: Interview personas, stage prompts, follow-up generation, closing
  feedback, interview dispatch bundles, capstone reviewer prompt templates,
  full capstone prompt bundles, provider-neutral LLM documentation, and prompt
  rendering tests.
- PROMPT_31: Administration Track A1 and A2; admin map with A1-A6 anchors,
  admin lesson/exercise tree support in the validator, 15 active admin lessons,
  120 admin exercises, admin seed SQL for role matrices and access reviews,
  admin-track docs/playbooks, and admin corpus/map tests.
- PROMPT_32: Administration Track A3 and A4; 17 active admin lessons, 136
  admin exercises, optional exercise `restore_drill` metadata, HBA overlay and
  PgBouncer Docker profiles, restore drill script, A3/A4 playbooks, lab docs,
  and admin/compose tests.

Next expected prompt:

- PROMPT_33: Administration Track A5 monitoring/performance operations and A6
  replication/HA operations.

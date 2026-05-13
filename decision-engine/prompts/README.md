# Decision-engine Prompt Pack

The decision-engine prompt pack is a provider-neutral set of Markdown templates
for authoring, cross-checking, and extending the deterministic planner. Prompts
use YAML front matter plus Jinja2 variables and are rendered by
`pgfound decision prompt render`; they do not call an LLM.

Layer 1, schema and catalog generation, helps maintainers propose new catalog
entries, intake-schema fields, and rule files without bypassing the engine's
schemas. The industry, data-shape, workload-pattern, extension, index-pattern,
topology-pattern, and anti-pattern prompts all require the relevant schema,
nearby entries, a concrete ask, and evidence. `refine-intake-schema` returns a
JSON Schema patch for one proposed field. `propose-rule` turns a real-world
scenario into a schema-shaped rule with `why_now`, `why_not_yet`, and
`triggers_for_next_stage`.

Layer 2, evaluator prompts, lets humans compare the deterministic engine with a
catalog-aware LLM pass. `evaluate-intake` renders a full intake, catalogs,
rules, and report schema into a report-shaped prompt. `explain-tradeoffs`
expands the narrative for a single recommendation. `generate-followup-questions`
prioritizes uncertainty-reducing questions for thin evidence. `generate-now-later-avoid`
turns an existing report into an executive one-pager while preserving the
engine's classes.

Layer 3, scenario prompts, supports regression-fixture authoring for fintech
payments, healthcare operations, SaaS multi-tenancy, ecommerce marketplaces,
logistics geo workloads, observability and IoT, knowledge AI, and modernization
bridge scenarios. Each prompt asks for a 300-500 word narrative, an intake JSON
object matching the schema, expected `recommend_now`, `candidate_later`, and
`avoid_for_now` outputs, and notes about the rules the fixture should exercise.

Layer 4, critique and validation prompts, challenges draft reports after the
engine has produced them. `cross-check-recommendations-against-anti-patterns`
maps recommendations to anti-pattern risks. `look-for-overcomplexity` checks
portfolio weight against operational tolerance. `test-portability-assumptions`
checks managed-service and portability constraints. `generate-benchmark-plan`
asks for a concrete validation plan before commitment. `identify-missing-core-features`
surfaces PostgreSQL core features that should be considered before heavier
choices.

The shared prompt `shared/system-prompt-architect` defines the senior
PostgreSQL architect persona used by the pack: conservative, operationally
aware, core-first, and unwilling to recommend anything without catalog and rule
citations. Shared output formats under `shared/output-formats/` define the
Markdown-plus-JSON contracts for catalog entries, rules, evaluator output,
scenario intakes, and critique findings.

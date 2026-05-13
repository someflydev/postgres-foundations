# Decision Engine Architecture

## Purpose and Scope

The decision engine is the structured planning subsystem for PostgreSQL
Foundations. Its job is to turn workload facts into explainable PostgreSQL
recommendations that a human architect can inspect, challenge, and improve. It
does not replace judgment. It narrows the conversation by making assumptions
visible, aligning recommendations with the project doctrine, and separating
evidence that exists now from evidence that would justify a later stage.

The engine is intentionally PostgreSQL core-first. A workload that needs tenant
isolation, search, retention, reporting, observability, or scale should first be
evaluated against core PostgreSQL capabilities: schemas, relational modeling,
constraints, transactions, isolation, indexing, partitioning, row-level security,
materialized views, replication, backup and restore practice, and operational
instrumentation. Extensions can be correct, but only when workload signals,
managed service constraints, team readiness, and portability tradeoffs support
the extra operating surface. "Not yet" is a first-class output because many
premature architecture decisions are expensive precisely because they solve a
future problem before the present system can measure it.

The subsystem now has catalog-backed rules and a validating runner. Catalogs
define the vocabulary, rules bind intake evidence to recommendations, and the
runner emits machine-readable and human-readable reports. The scoring model is
still intentionally simple until the next prompt replaces it with a fuller
weighted model.

## Inputs

The first input is a workload intake. The intake is a JSON document with an
`intake_id`, an `as_of_date`, organization constraints, data shapes, workload
patterns, scale signals, tenancy model, security requirements, migration or
federation needs, existing topology, explicit extension biases, and free-form
notes. The schema is deliberately factual. It asks for observable signals such as
largest table row counts, write throughput, read QPS, peak connections, object
size, and month-over-month growth. It also records human constraints such as
managed service requirements, portability boundaries, operational tolerance, and
team size. Those human constraints are not secondary. A recommendation that a
small team cannot operate is not a good recommendation.

The second input class is catalog data. Catalogs describe industries, data
shapes, workload patterns, core features, extensions, index patterns, topology
patterns, and anti-patterns. These catalogs are shared with the extension track
so that training material and automated planning use the same vocabulary. A
catalog entry is not just a label. It will eventually contain applicability
signals, operational costs, portability notes, references to lessons or
playbooks, and failure modes. This lets the engine explain why a capability is
relevant instead of merely naming it.

The third input class is rules. Rules connect intake signals and catalog entries
to recommendations. They express conditions, confidence, explanation text,
thresholds, and anti-pattern checks. Rules should be small, auditable, and
testable. A reviewer can inspect a recommendation, trace it to rule IDs, and
decide whether the rule overreached or whether the intake is missing important
facts.

Rule predicates use this vocabulary:

- `industry_is` and `industry_in`
- `data_shape_present`, `data_shape_any_of`, and `data_shape_all_of`
- `workload_pattern_present` and `workload_pattern_any_of`
- `scale_signal_gte` and `scale_signal_lt`
- `tenancy_model_is` and `tenancy_model_in`
- `security_constraint_present`
- `portability_constraint_present`
- `operational_tolerance_is`
- `existing_topology_is`
- `migration_need`
- `free_form_notes_contains`
- `explicit_bias_for_contains`
- `explicit_bias_against_contains`

The scale predicates accept observed intake scale fields and the derived key
`largest_table_rows`, which is the maximum value from
`row_counts_largest_tables`.

## Processing Model

The processing pipeline begins with schema validation. An invalid intake stops
the run because downstream reasoning needs a trustworthy shape. Once the intake
is valid, the engine validates catalog references, loads every rule file, and
validates each rule against `rule.schema.json`. Rule linting also checks catalog
targets, duplicate rule IDs, known predicate operators, simple contradictory
conditions, and extension catalog coverage.

The first real reasoning stage is rule matching. A rule can match industry,
data-shape, workload-pattern, scale, tenancy, security, migration, topology, and
explicit-bias signals. Matching should produce candidate recommendation evidence,
not a final answer. For example, a multi-tenant shared-schema SaaS intake with
`rls_required` may produce evidence for row-level security as a core feature,
tenant-scoped compound indexes as an index pattern, and an anti-pattern warning
against application-only tenant filtering. A large time-ordered event workload
may produce evidence for partitioning, but the verdict depends on growth,
retention, query pruning, maintenance readiness, and managed service support.

The second stage turns matched evidence into recommendations with confidence.
Confidence is a bounded 0 to 1 value that communicates how strongly the known
signals support the recommendation. It is not probability. It is a compact
summary of evidence quality, rule agreement, and missing information. Each
recommendation carries `why_now`, `why_not_yet`, and
`triggers_for_next_stage`. This structure forces the engine to explain both
positive and negative reasoning. A recommendation for core RLS should explain
tenant isolation and auditability. A "candidate later" verdict for Citus should
explain what is missing now and which measurable scale or distribution signals
would change the answer.

The third stage scores the overall fit. The report schema reserves score slots
for domain fit, data-shape fit, workload fit, operational feasibility, growth
urgency, portability penalty, and complexity penalty. Scores are intentionally
separated so that a high workload fit can be offset by weak operational
feasibility or a strong portability penalty. This keeps the engine from hiding a
tradeoff in a single opaque number.

The fourth stage runs anti-pattern checks. Anti-patterns are warnings, not
automatic vetoes. They catch common mistakes such as adding distributed
architecture without a distribution key, choosing an extension before core
PostgreSQL has been tested, relying on application-only tenant filters where RLS
is required, or adding indexes without a query and maintenance story. The final
stage assembles the machine-readable report and the human-readable Markdown
report.

## Outputs

The primary output is `report.json`, a machine-readable document that validates
against `report.schema.json`. It contains the intake ID, generation timestamp,
engine version, recommendations, score breakdown, warnings, and follow-up
questions. The recommendation entries include target kind, target slug, verdict,
confidence, explanation arrays, next-stage triggers, and rule-source
contributions. Later prompts will use these reports as golden fixtures for
regression tests.

The secondary output is `report.md`, a human-readable sibling. Markdown is not
the source of truth, but it is the artifact a learner, reviewer, or architect can
read quickly. It should preserve the same structure as the JSON: what the engine
recommends now, what remains a candidate, what should be avoided for now, which
warnings matter, and what questions a human should answer before committing to a
design.

## Composition with Training and Interviews

The decision engine composes with the training platform by sharing doctrine,
catalog terms, and examples. Curriculum lessons teach the human version of the
same reasoning: use workload evidence, understand PostgreSQL core features, and
avoid extensions until the operational case is concrete. Extension-track modules
can point to the same catalog entries the engine uses, which prevents drift
between what the course teaches and what the planner recommends.

It also composes with the review engine and interview simulator. A capstone or
exercise reviewer can compare a learner's architecture against decision-engine
signals without treating the engine as the judge. The interview scenario
`architect-decision-engine-review` can ask a candidate to critique a generated
report: which recommendation is under-supported, which "not yet" threshold is
too vague, which operational cost is missing, and what additional workload facts
would change the decision. This makes the engine a practice object as well as a
planning tool.

## Keeping the Engine Honest

The engine stays honest through testable artifacts. Golden intakes and reports
make output drift visible. Schema validation prevents malformed input and report
shape changes from sneaking through. Rule auditability requires every
recommendation to cite rule IDs and contribution values. Explicit "not yet"
thresholds prevent vague deferral. A future-stage trigger should be measurable:
row count, retention window, write rate, query latency, replica lag, restore
objective, tenant count, managed service support, or team operational maturity.

Rules should be biased toward conservative recommendations when evidence is
thin. `not_enough_evidence` is a useful verdict because many planning questions
are under-specified. `avoid_for_now` is appropriate when the intake shows a
clear mismatch, such as mandatory managed-service portability against an
extension unavailable on the target platforms. The engine should also preserve
explicit team bias without obeying it blindly. A team may be committed to an
extension, but the report still needs to name the operational and portability
costs.

## Versioning and Evolution

The report includes an `engine_version` so downstream tests, prompt packs, and
human reviewers can tell which rule set produced an artifact. Schema changes
should be additive when possible. A new catalog field can be optional until the
catalog authoring prompts and report goldens are updated. A breaking intake or
report change should be paired with fixture migration and explicit documentation
because these files become part of the teaching contract. Catalog entries and
rules should evolve through small reviewable changes: add the workload signal,
add or update the rule, update the golden report, then document the new behavior
where learners or interview reviewers will encounter it. This keeps the engine
from becoming a hidden policy store that only the implementation understands.

## Limits

The decision engine is a structured reasoning tool, not an oracle. It cannot
infer missing business context, prove future scale, or replace production
measurement. It cannot know whether a team has practiced restores, whether an
on-call rotation can handle a new topology, or whether a managed service has a
region-specific limitation unless those facts are present in the intake or
catalogs. It should therefore end reports with follow-up questions when facts
are missing.

A human architect is always the final decision-maker. The engine is successful
when it makes that human's work clearer: fewer hidden assumptions, better
tradeoff language, stronger links between workload evidence and PostgreSQL
capabilities, and more disciplined triggers for adopting complexity later.

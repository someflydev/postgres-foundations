# Architecture

`postgres-foundations` is one platform made from three interlocking
subsystems: the curriculum and training system, the administration + extension
mastery track, and the decision engine. They share doctrine,
artifacts, and review expectations so that learning PostgreSQL and planning
PostgreSQL architecture reinforce the same operating model.

```text
                 +--------------------------------+
                 | Shared doctrine and artifacts  |
                 | docs/, rubrics/, catalogs,     |
                 | scenarios, prompt templates    |
                 +---------------+----------------+
                                 |
          +----------------------+----------------------+
          |                      |                      |
+---------v----------+  +--------v---------+  +---------v----------+
| Curriculum and     |  | Administration   |  | Decision engine    |
| training system    |  | and extension    |  | catalogs, rules,   |
| lessons, labs,     |  | mastery track    |  | scoring, reports   |
| review, capstones  |  | A1-A6, E1-E7     |  |                    |
+---------+----------+  +--------+---------+  +---------+----------+
          |                      |                      |
          +----------------------+----------------------+
                                 |
                    Review, defense, and planning
```

## Curriculum and Training System

The curriculum and training system teaches PostgreSQL from first contact
through practical competence. Its scope includes phases 0-10, capstones, a
review engine, an interview simulator, a local Docker lab, a rubric corpus, and
progress concepts. It is not a passive content library. It is a training system
that requires learners to produce work, inspect PostgreSQL behavior, explain
their reasoning, and repair flawed designs.

Its inputs are phase definitions, lessons, exercises, seed data, scenarios,
rubrics, learner submissions, database observations, and LLM prompt templates.
Its outputs are completed labs, reviewed answers, oral defenses, progress
signals, remediation paths, and capstone evaluations. The training loop should
produce evidence of competence rather than a simple count of completed pages.

The main artifacts live under `curriculum/`, `lessons/`, `exercises/`,
`seed-data/`, `scenarios/`, `rubrics/`, `capstones/`, `llm-prompts/`, `docker/`,
and `tests/`. Early prompts may leave many of these directories skeletal, but
their roles are fixed by this architecture. The local package under `src/`
provides command-line and programmatic support as the platform grows.
Authoring rules, required fields, examples, and validator behavior are captured
in [Content Authoring](authoring.md).

Reusable scenario domains live under `seed-data/packs/`. These packs define the
small canonical schemas, seed rows, manifests, and deterministic generators for
domains such as ecommerce, scheduling, SaaS multi-tenancy, event-heavy
operations, document search, and modernization. Lessons can use the early
phase SQL directly, while scenarios and capstones reuse the same domain shapes
when they add constraints, query tuning, concurrency, operations, or planning
requirements. Naming rules for these packs are documented in
[Domain Conventions](domain-conventions.md).

The learner flow begins with guided recognition and controlled production,
then moves toward independent production, critique, and repair. A learner reads
a lesson, works in the Docker lab, runs SQL, inspects errors and plans, submits
an answer, receives review, and defends the design. Capstones combine multiple
skills and require the learner to handle ambiguity, failure, and operational
constraints.

Capstones are the clearest cross-subsystem exercise. They pull curriculum
skills, administration practice, extension posture, scenario harnesses, rubrics,
and decision-engine doctrine into one artifact. A capstone submission is not
only a schema or a set of queries; it is a small planning record that explains
which PostgreSQL core features are enough now, which extensions or topologies
are deferred, and what operational evidence would change the recommendation.

The coach or reviewer flow starts from a learner artifact. The reviewer uses
rubrics, expected observations, and prompt templates to evaluate correctness,
explanation quality, operational awareness, and repair ability. The interview
simulator uses the same doctrine to ask follow-up questions rather than simply
marking answers right or wrong.

The curriculum interlocks with the administration and extension track by making
core mastery a prerequisite for advanced operational and extension work. It
interlocks with the decision engine by teaching the same reasoning that the
engine later encodes: core first, explain why, name "not yet", and attach every
recommendation to workload signals.

## Administration + Extension Mastery Track

The administration and extension mastery track covers operational PostgreSQL
and selected extensions after core competence is established. It includes admin
modules A1-A6 and extension modules E1-E7, plus specific treatment of `ltree`,
`pg_partman`, and PgBouncer. The scope is deliberately downstream of core
mastery: learners first understand schemas, transactions, indexes, query
plans, and basic operations before taking on replication, backups, security,
maintenance, pooling, partition management, or extension-specific tradeoffs.

Its inputs are the core curriculum outcomes, operational scenarios, failure
drills, extension catalogs, topology patterns, anti-patterns, and production
style constraints. Its outputs are lab completions, runbook-ready explanations,
extension selection defenses, operational checklists, incident responses, and
capstone artifacts that prove the learner can run PostgreSQL systems rather
than merely query them.

The main data artifacts live primarily under `curriculum/`, `lessons/`,
`exercises/`, `scenarios/`, `rubrics/`, `capstones/`, `docker/`, and later
extension references that point into `decision-engine/catalogs/extensions.json`.
PgBouncer belongs in both the learning track and the planning vocabulary
because it is a common operational answer to connection pressure, but it still
requires context: pooling mode, transaction behavior, application assumptions,
and observability.

The learner flow in this track is more operational than syntactic. Learners
perform backups and restores, diagnose bloat, reason about replication lag,
practice role and privilege design, evaluate pooling, and decide when an
extension is justified. Extension work must include a core alternative, a
workload trigger, and an operational consequence.

The coach or reviewer flow emphasizes defense under realistic constraints. The
reviewer should ask whether the learner can explain what fails during restore,
what changes under write load, why an extension is appropriate now, and what
would make the design portable or less portable.

This track interlocks with the curriculum by extending the same scaffolding
levels into operations. It interlocks with the decision engine through shared
catalogs and anti-patterns. If the decision engine says `pg_partman` is "not
yet" until retention and partition maintenance signals appear, the extension
track should teach the learner to reach the same conclusion manually.

## Decision Engine

The decision engine turns workload descriptions into explainable PostgreSQL
planning guidance. Its scope includes JSON catalogs for industries,
`data_shapes`, `workload_patterns`, `postgres_core_features`, extensions,
`index_patterns`, `topology_patterns`, and anti-patterns; rules; scoring; an
evaluator; and a report generator. It also includes the four-layer
decision-engine prompt pack that supports structured planning conversations
and review.

Its inputs are structured workload descriptions, catalog data, rules, scoring
weights, anti-pattern definitions, and prompt templates under
`decision-engine/prompts/`. Its outputs are human-readable reports, ranked
recommendations, "why now" and "why not yet" explanations, trigger conditions
for future stages, warnings about operational burden, and references back to
core PostgreSQL features or extension choices.

The main artifacts live under `decision-engine/catalogs/`,
`decision-engine/rules/`, `decision-engine/prompts/`, and future evaluator and
reporting modules in `src/`. Catalogs are JSON-first so they can be validated,
diffed, tested, and reused by both the planning engine and the learning
materials. YAML may be tolerated only where human ergonomics clearly justify
it, but JSON is the default for content and decision data.

The architect or planner flow starts with workload facts: domain, data shape,
read/write pattern, latency needs, retention, search behavior, geography,
connection profile, operations maturity, portability constraints, and team
experience. The evaluator maps those facts to core features, index patterns,
topology options, extensions, and anti-pattern checks. The report generator
then explains recommendations in operational language, including why a feature
is appropriate, why another feature is not yet appropriate, and what evidence
would change the result.

The coach or reviewer flow uses the engine as an object of critique. A reviewer
can ask whether the report overreaches, whether the workload evidence supports
the recommendation, whether the "not yet" triggers are measurable, and whether
the operational consequences are explicit.

The decision engine interlocks with the curriculum because it formalizes the
same reasoning learners practice in labs and capstones. It interlocks with the
administration and extension track because its catalogs are the planning
version of the same extension and topology knowledge taught in advanced
modules. No subsystem owns doctrine alone; each one exercises it from a
different user role.

## Shared Artifacts and Boundaries

Shared artifacts should be referenced rather than copied. Doctrine lives in
`docs/doctrine.md`. Architecture lives in this document. ADRs live in
`docs/adr/`. Rubrics live under `rubrics/`. Training prompts live under
`llm-prompts/`; planning prompts live under `decision-engine/prompts/`.
Decision metadata such as extension characteristics should become
authoritative in `decision-engine/catalogs/` and be referenced from training
materials.

The boundary between subsystems is practical, not ideological. Curriculum
teaches people. The administration and extension track teaches operational and
advanced capability after core mastery. The decision engine evaluates workload
signals and produces planning guidance. Their overlap is intentional where it
keeps language, catalogs, rubrics, and doctrine consistent.

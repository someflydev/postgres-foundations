# LLM Usage

LLMs participate in `postgres-foundations` as structured training and planning
assistants. They are useful when they increase review pressure, require clearer
reasoning, or generate targeted remediation from work the learner or planner
has already attempted. They are harmful when they replace the direct practice
that the platform exists to create.

## Roles

As a coach, an LLM can ask guiding questions, identify a likely misconception,
and suggest the next drill after seeing a learner's attempt. The coaching role
should preserve learner agency: it should point the learner back to PostgreSQL,
plans, errors, and evidence rather than provide a polished answer too early.

As a reviewer, an LLM can compare a submission against a rubric, test whether
the explanation matches the SQL or schema, and call out missing operational
concerns. Review should address correctness, reasoning, portability, and the
ability to repair weak choices.

As an interviewer, an LLM can simulate oral defense. It can ask why a learner
chose an index, what would happen under concurrency, how a migration might
fail, or how restore practice changes confidence in a backup plan. Interview
mode is valuable because competence includes explanation under pressure.

As an adversary, an LLM can challenge assumptions. It can present edge cases,
failure modes, workload changes, or anti-pattern checks. This role helps
learners and planners move beyond a single happy-path answer.

As a remediation generator, an LLM can produce focused follow-up exercises from
observed mistakes. Remediation should be narrow, tied to evidence, and aimed at
the missing capability layer rather than generic repetition.

## Anti-Roles

An LLM must not be the learner's first-pass answer machine. If the learner has
not attempted the query, schema, diagnosis, or design, the LLM should ask for an
attempt or redirect them into the lab.

An LLM must not act as a SQL or schema bypass. The platform teaches direct work
with PostgreSQL, so generated SQL is only useful when the learner can run it,
inspect it, explain it, and revise it.

An LLM must not replace direct PostgreSQL interaction. It cannot substitute for
reading an execution plan, observing locks, checking catalog views, performing a
restore, or watching a query fail.

An LLM must not replace multi-session concurrency labs. Concurrency,
transaction isolation, locks, deadlocks, and waiting behavior must be observed
in real sessions.

## When LLMs Help or Harm

LLM involvement improves learning after evidence exists: a draft answer, a
failed query, a schema proposal, an execution plan, a restore transcript, or a
planning report. At that point the LLM can review concrete work, ask for a
defense, and generate targeted remediation.

LLM involvement harms learning when it collapses struggle before the learner
has formed a model. It also harms planning when it jumps to a fashionable
capability without workload signals. The platform should prefer prompts that
ask "what evidence supports this" and "what would make this not yet" over
prompts that ask for broad solution lists.

## Prompt Locations

Training-side prompt templates live in `llm-prompts/`. They support coaching,
review, interview simulation, adversarial critique, and remediation against
lessons, labs, rubrics, and capstones. These prompts should reference learner
artifacts and rubrics rather than asking the model to invent curriculum
standards.

Training-side templates are Markdown files with YAML front matter. The
front matter declares the template `id`, title, consumers, required inputs,
output-format contract, model hint, and default variables. The body is rendered
with Jinja2 against a JSON context. The canonical format is documented in
`llm-prompts/template-format.md`.

Use `pgfound llm list` to inspect templates and `pgfound llm render
<template-id> --context <json-file>` to render one. Rendering is the contract:
the CLI writes a prompt to stdout or `--out` and never calls a model.

Planning-side prompt templates live in `decision-engine/prompts/`. They support
structured workload intake, catalog-aware evaluation, report critique, and
decision explanations. These prompts must stay aligned with decision-engine
catalogs and rules so planning guidance remains explainable, operationally
aware, and core-first.

Use `pgfound decision prompt list` to inspect planning templates and
`pgfound decision prompt render <template-id> --context <json-file>` to render
one. The decision prompt pack has four layers: schema and catalog generation,
evaluator cross-checks, industry scenario generation, and critique/validation.
The shared architect persona requires every recommendation to cite rules or
catalog entries and permits "not yet" when evidence or operational tolerance is
insufficient.

In both locations, prompt templates should make the LLM's role explicit. The
model is there to review, question, challenge, and remediate. It is not there to
replace the lab, the database, or the planner's responsibility to defend a
recommendation.

## Interview Stub Behavior

`pgfound interview start --scenario <id>` uses templates from
`llm-prompts/interview/stages/`, but Prompt 28 does not make real LLM calls. For
each stage, the simulator prints the resolved prompt, records the learner's
response, logs the exact payload it would send to the LLM, and emits the stub:

```text
[LLM response intentionally stubbed until PROMPT_30 interview integration]
```

Design and explainability stages also close with standard follow-up questions
from the prompt template. Debugging drill stages reference existing exercises
and attempt the normal exercise check against the learner's saved answer.

PROMPT_30 should plug into this by upgrading interview-specific prompts while
continuing to keep the actual model call stubbed. The transcript format and the
"what would be sent" audit trail should remain stable so review and replay
tooling can compare stubbed and real interviewer behavior later.

## Rendered Review Artifacts

`pgfound exercise review --full` writes deterministic review reports and also
renders `critique/query-critique` to `prompt.md` in the review output directory.
The prompt includes the learner SQL, reference SQL, rubric id, allowed concept
lists, and mechanical findings.

`pgfound capstone evaluate --full` renders schema and index critique prompts
next to the capstone review reports. These prompts remain audit artifacts until
a future provider-specific dispatch layer is added.

# Interview Simulator

The interview simulator lets learners practice explaining and defending
PostgreSQL design decisions. The interviewer voice is still stubbed, but each
stage renders the same provider-neutral LLM prompt that an external dispatch
layer can send to a model. The session prints the rendered stage prompt, records
the learner response, logs the prompt and canned stub response, and writes a
transcript for deterministic rubric review.

## Commands

Start a session:

```bash
uv run pgfound interview start --scenario senior-backend-saas-rls
```

Review an existing transcript:

```bash
uv run pgfound interview review tmp/interviews/senior-backend-saas-rls/<timestamp>.md
```

Print a single prompt bundle for an external LLM CLI:

```bash
uv run pgfound interview dispatch tmp/interviews/senior-backend-saas-rls/<timestamp>.md
```

Transcripts are written under `tmp/interviews/<scenario-id>/<timestamp>.md`.

## Session Flow

Interview scenarios live in `scenarios/interviews/*.yaml` and validate against
`content-schemas/interview-scenario.schema.json`.

Each scenario has a duration, required capability layers, stages, and an
interview rubric. Stage kinds are:

- `warmup`: establishes assumptions and domain shape.
- `design_probe`: asks the learner to defend a design topic.
- `debugging_drill`: references an existing exercise and attempts the exercise
  check against the learner's saved answer.
- `explainability`: asks for an oral defense with tradeoffs and not-yet
  posture.

Learner input is multi-line. End a stage with `/next`; EOF ends the current
stage and any remaining session input.

## Prompt Templates

Stage templates live under `llm-prompts/interview/stages/` and use the same
YAML-front-matter/Jinja2 format as the rest of `llm-prompts/`. Persona prompts
live under `llm-prompts/interview/personas/`; the simulator chooses the
adversarial architect persona for `architect-decision-engine-review`, the
mid-level persona for mid-level scenarios, and the senior persona otherwise.

The simulator renders the warmup prompt, the persona prompt after warmup, every
configured scenario stage, the follow-up generator for probing stages, and a
closing-feedback prompt over the full transcript. Hidden simulator notes are
delimited with `=== HIDDEN SIMULATOR NOTES ===` so a future live simulator can
strip them before showing output to learners.

## Transcript Contract

Every transcript follows this shape:

```markdown
# Interview: <title>
- scenario_id: ...
- started_at: ...
- completed_at: ...
- learner: ...

## Persona Prompt
...

## Stage: warmup
### Prompt
...
### Learner response
...
### Simulator notes
...
```

`pgfound.interview.transcripts.validate_transcript()` parses this structure so
review tooling and `pgfound interview dispatch` can consume the file without
scraping arbitrary Markdown.

## Rubrics

Interview rubrics live under `rubrics/interview/` and set
`applies_to: interview`. The current evaluator is deterministic and deliberately
weak: it looks for transcript signals such as enough explanatory detail,
because-style justification, tradeoff language, correctness vocabulary, and
operational/not-yet posture. LLM prompts remain provider-neutral artifacts; the
local simulator does not call a model.

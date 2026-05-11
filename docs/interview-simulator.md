# Interview Simulator

The interview simulator lets learners practice explaining and defending
PostgreSQL design decisions. Prompt 28 keeps the interviewer voice stubbed:
the session prints the stage prompt, records the learner response, logs the
payload that would be sent to an LLM, and writes a transcript for deterministic
rubric review.

## Commands

Start a session:

```bash
uv run pgfound interview start --scenario senior-backend-saas-rls
```

Review an existing transcript:

```bash
uv run pgfound interview review tmp/interviews/senior-backend-saas-rls/<timestamp>.md
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

Stage templates live under `llm-prompts/interview/stages/`. Templates may use
these placeholders:

- `{scenario_id}`
- `{scenario_title}`
- `{stage_kind}`
- `{topic}`
- `{exercise_id}`
- `{exercise_prompt}`

Templates may include a `## Follow-ups` section with bullet questions. The
session prints those follow-ups for design and explainability stages and records
them in simulator notes.

## Transcript Contract

Every transcript follows this shape:

```markdown
# Interview: <title>
- scenario_id: ...
- started_at: ...
- completed_at: ...
- learner: ...

## Stage: warmup
### Prompt
...
### Learner response
...
### Simulator notes
...
```

`pgfound.interview.transcripts.validate_transcript()` parses this structure so
future review tooling can consume the file without scraping arbitrary Markdown.

## Rubrics

Interview rubrics live under `rubrics/interview/` and set
`applies_to: interview`. The current evaluator is deterministic and deliberately
weak: it looks for transcript signals such as enough explanatory detail,
because-style justification, tradeoff language, correctness vocabulary, and
operational/not-yet posture. PROMPT_30 can add interview-specific rendered
prompts without changing the transcript contract.

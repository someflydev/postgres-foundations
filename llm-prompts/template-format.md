# Template Format

Each training-side LLM template is a Markdown file with YAML front matter.

Required front-matter fields:

- `id`: path-like template id without `.md`, for example `critique/query-critique`.
- `title`: short human-facing title.
- `consumed_by`: CLI flows or tools expected to render the template.
- `inputs`: mapping of context keys to `{ required: true|false, kind: ... }`.
- `outputs.format`: name of a shared output contract under
  `llm-prompts/shared/output-formats/`.

Optional fields:

- `model_hint`: non-binding capability guidance for a future dispatch layer.
- `variables`: default values merged before context JSON and `--var` overrides.

Rendering uses Jinja2. Required inputs are validated before rendering. The CLI
does not call an LLM; it only writes the final prompt text to stdout or `--out`.

Template sections should usually be:

```markdown
## System

Role, doctrine, and refusal boundaries.

## Context

Rendered learner, lesson, rubric, stage, or workload context.

## Inputs

Quoted learner artifacts and deterministic engine findings.

## Instructions

Specific review, coaching, or remediation tasks.

## Output Format

Reference to a shared output-format file.
```

Prompts should preserve self-directed practice. When a learner has not made an
attempt, the model should ask for one or offer a minimal next observation step
rather than solving the exercise.


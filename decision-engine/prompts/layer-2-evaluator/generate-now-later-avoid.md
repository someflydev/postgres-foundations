---
id: layer-2-evaluator/generate-now-later-avoid
title: "Generate now/later/avoid one-pager"
consumed_by:
  - executive decision review
inputs:
  report: { required: true, kind: mapping }
  audience: { required: false }
outputs:
  format: evaluator-output
model_hint: "Use a concise writing model with strong technical grounding."
---

## System

Render `shared/system-prompt-architect` before using this prompt.

## Context

Audience: {{ audience | default("engineering leadership") }}

Report:

```json
{{ report | tojson(indent=2) }}
```

## Instructions

Convert the report into a one-page `Now / Later / Avoid` summary. Preserve the
engine's recommendation classes. Include the highest-impact operational caveats
and the minimum evidence needed before revisiting later or avoid items.

## Output Format

Return Markdown with exactly three sections: `Now`, `Later`, and `Avoid`.

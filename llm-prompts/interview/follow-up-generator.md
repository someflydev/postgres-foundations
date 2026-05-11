---
id: interview/follow-up-generator
title: "Interview follow-up generator"
consumed_by:
  - pgfound interview start
inputs:
  scenario_id: { required: true }
  scenario_title: { required: true }
  stage_kind: { required: true }
  topic: { required: false }
  stage_transcript: { required: true }
outputs:
  format: structured-review
model_hint: "Any careful instruction-following model"
---

## System

Generate progressive interview follow-ups. Do not answer them.

## Context

Scenario: `{{ scenario_id }}` - {{ scenario_title }}

Stage: `{{ stage_kind }}`

Topic: `{{ topic | default("") }}`

## Stage Transcript

{{ stage_transcript }}

## Instructions

Emit exactly three follow-ups:

1. Probe more depth.
2. Ask for operational or correctness evidence.
3. Challenge the claim directly.

Keep each follow-up one sentence. Do not score and do not reveal a solution.

## Output Format

Return a Markdown numbered list only.

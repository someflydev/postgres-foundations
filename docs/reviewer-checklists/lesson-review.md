# Lesson Review Checklist

Use this checklist when reviewing a lesson before it becomes active or when
updating a mature lesson.

## Content Fit

- The lesson teaches one clear capability and names the learner's starting
  assumption.
- The material matches the phase/module scope and does not jump ahead without a
  deliberate forward pointer.
- PostgreSQL core behavior is explained before extensions, topology, or vendor
  conveniences.
- Examples are concrete enough to run or reason about in the lab domain.

## Operational Quality

- The lesson names failure modes, edge cases, or maintenance implications where
  they matter.
- Tradeoffs are explicit. The lesson does not imply that an index, constraint,
  extension, or topology choice is universally correct.
- Any "not yet" guidance names what evidence would change the recommendation.

## Authoring Quality

- References resolve to existing docs, exercises, ADRs, or external sources.
- Forbidden concepts and future topics are not taught before their phase.
- The worked example, if present, is aligned with the lesson objective.
- The lesson points to at least one exercise that practices the taught skill.

## Review Output

Record required fixes as actionable edits, not vague taste feedback. If the
lesson is acceptable with caveats, name the caveat and the future prompt/module
where it should be revisited.

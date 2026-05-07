# Lesson Authoring Guide

Lessons live under `lessons/phase-NN-phase-slug/<cluster>/<lesson-slug>/`.
Create them with the scaffold command so directory names, `lesson.json`, and
`body.md` start from the shared conventions:

```sh
uv run pgfound content scaffold lesson \
  --phase 7 \
  --cluster btree-and-composite-indexes \
  --slug btree-composite-vs-single-column \
  --title "B-tree: composite vs single-column indexes" \
  --capability-layer indexing_and_plans
```

The scaffold command reads `curriculum/map.json`, creates the lesson directory,
writes `lesson.json` from
`content-schemas/templates/lesson.json.template`, writes `body.md` from
`content-schemas/templates/lesson-body.md.template`, and validates the new draft.

## Authoring Flow

1. Run `pgfound content scaffold lesson` with the target phase, cluster, slug,
   title, and capability layer.
2. Fill `lesson.json`: summary, objectives, introduced concepts, forbidden
   concepts, references, tags, and exercise ID arrays.
3. Fill `body.md` using the seven required sections from the template.
4. Add a `worked-example.md` only when the worked example needs to stand apart
   from the main body.
5. Run validation and lint while the lesson is still `draft`.
6. Add exercises that reference the lesson ID.
7. Flip `status` to `active` only after placeholders are gone.

## Active Checklist

- `lesson.phase` matches the `phase-NN-...` directory.
- `body_path` points to an existing `body.md` in the lesson directory.
- No `__REPLACE_ME__` placeholders remain in `lesson.json` or `body.md`.
- `concepts_introduced` and `concepts_not_yet_allowed` do not overlap.
- `body.md` has all seven required sections.
- Active body text is at least 400 words.
- Links use titled markdown syntax, not bare URLs.
- No TODO, TBD, or XXX tokens remain.
- At least one exercise references this lesson ID.

## Checks

```sh
uv run pgfound content validate --paths 'lessons/**/lesson.json'
uv run pgfound content lint --strict --paths 'lessons/**/lesson.json'
```

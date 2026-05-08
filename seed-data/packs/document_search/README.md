# Document Search

## What this domain is

The document search domain models a small knowledge base with documents, authors, and tags. It lets learners begin with ordinary rows before they face document bodies, metadata, and search behavior. Later phases can upgrade the same domain with JSONB boundaries, full-text search, ranking, and indexing.

## Core entities

- Authors: people or teams that own documents.
- Documents: searchable pieces of knowledge with titles and bodies.
- Tags: labels that group documents for navigation.
- Document tags: a many-to-many bridge introduced for joins.

## Recurring scenarios

- Phase 0: model authors, documents, tags, many-to-many tag links, publication
  state, and archival events on paper before SQL.
- Phase 1: filter and sort published documents.
- Phase 2: join documents to authors and tags.
- Phase 4: compare relational columns with JSONB metadata.
- Phase 5: rank search results and summarize document coverage.
- Phase 7: tune search and tag-filter queries.
- Phase 10: reuse the knowledge-base shape in capstone design.

## Non-goals

This pack does not teach search engines, vector databases, crawling, permissions, or editorial workflows. It keeps the focus on PostgreSQL-native representation and query behavior.

## Naming and schema overview

Large labs use the `documents` schema. Small exercises may collapse these tables into `pgfound`. Tables: `authors`, `documents`, `tags`, and `document_tags`.

## Generators

Run `python generators/documents_csv.py` from this pack to print deterministic CSV rows for larger search exercises. The current seed SQL remains intentionally small.

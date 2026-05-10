# Event-Heavy Ops

## What this domain is

The event-heavy operations domain models append-only operational events from services and devices. It starts as a small event log that learners can filter by type and time. Later phases use the same shape to discuss grouping, ingestion volume, indexes, retention, and partitioning without inventing a new workload.

## Core entities

- Sources: systems that emit events.
- Events: append-only facts with type, timestamp, and JSON payload.
- Incident links: relationships from events to operational incidents introduced for joins.

## Recurring scenarios

- Phase 0: model sources, events, incident links, event identity, and lifecycle
  facts on paper before SQL.
- Phase 1: inspect recent events by source and type.
- Phase 2: group events by source and join to incident context.
- Phase 4b: add `event_windows` with `tstzrange` and a GiST index pointer for
  append-heavy time-window questions.
- Phase 5: derive rolling counts and latest event per source.
- Phase 7: tune time-ordered event queries.
- Phase 8: discuss operational visibility for ingest-heavy tables.
- Phase 9: partition events by event time.

## Non-goals

This pack does not implement a message broker, exactly-once delivery, tracing system, or metrics backend. PostgreSQL is treated as the teaching surface for durable operational facts.

## Naming and schema overview

Large labs use the `events` schema. Small exercises may collapse these tables into `pgfound`. Tables: `sources`, `events`, and `incident_events`.

## Generators

Run `python generators/events_csv.py` from this pack to print deterministic CSV rows for larger event exercises. The seed CLI can run generators with `--generate`; current phase SQL remains small and self-contained.

Phase 05 volume: at least 50000 deterministic generated events across checkout, billing, catalog, identity, and notifications sources.

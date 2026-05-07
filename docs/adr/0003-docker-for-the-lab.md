# Docker for the Lab

## Status

Accepted

## Date

2026-05-07

## Context

Learners need to run PostgreSQL drills, failure scenarios, restore practice,
and eventually multi-session labs without hand-building a local database
environment. The platform must work across macOS and Linux and should make lab
state reproducible enough for tests, rubrics, and support instructions.
Expecting every learner to install and tune PostgreSQL locally would introduce
irrelevant setup variance.

## Decision

Use Docker Compose as the canonical PostgreSQL lab environment. Learners are
not expected to install PostgreSQL directly on their machines for ordinary
platform use. The lab should define services, volumes, seed data, and reset
paths in repository-controlled files under `docker/` and related scripts.

## Consequences

Labs become more reproducible and easier to reset. Instructions can target the
same service names and ports across supported development machines. The project
must maintain Compose files carefully, keep macOS and Linux behavior in view,
and avoid hiding PostgreSQL behavior behind unnecessary wrappers. Docker
becomes a contributor prerequisite for lab work, although documentation and
static validation can still be read without it.

## Alternatives considered

Local PostgreSQL installation was rejected as the default because system
packages, versions, authentication, and service management vary too much.
Cloud-hosted lab databases were rejected for the core lab because they add
cost, network dependency, and weaker reset control. Embedded database
substitutes were rejected because the platform teaches PostgreSQL specifically.

## Related ADRs/docs

- [Architecture](../architecture.md)
- [Repo layout](../repo-layout.md)

# Scheduling

## What this domain is

The scheduling domain models appointments between providers and clients. It gives learners concrete time-based rows before introducing availability, overlap rules, and transaction safety. The same simple appointment book can later expose time zone mistakes, range modeling, and concurrent booking conflicts.

## Core entities

- Providers: people or resources that can be booked.
- Clients: people requesting appointments.
- Appointments: scheduled meetings with start and end times.
- Availability blocks: bookable windows introduced when joins and time ranges matter.

## Recurring scenarios

- Phase 0: model providers, clients, appointments, availability, overlap rules,
  and cancellation events on paper before SQL.
- Phase 1: inspect upcoming appointments.
- Phase 2: join appointments to providers and clients.
- Phase 3: reject invalid appointment status, impossible durations, and duplicate
  provider start times.
- Phase 4: model event time, professional time zones, availability ranges, and
  multirange working calendars.
- Phase 6: reason about two sessions booking the same slot.
- Phase 8: inspect locks and operational symptoms around hot schedules.

## Non-goals

This pack does not implement calendar invitations, reminder delivery, billing, or full recurrence rules. Recurrence appears only if a later lesson needs it as a modeling tradeoff.

## Naming and schema overview

Large labs use the `scheduling` schema. Small exercises may use `pgfound` when schemas would distract from the lesson. Tables: `providers`, `clients`, `appointments`, and `availability_blocks`.

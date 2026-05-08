# Identity Without IDs

## Problem Framing

Phase 0 starts with reality rather than syntax. A learner should be able to read a short description of a migration from legacy customer and order records into clearer target facts and say what facts the organization is trying to remember before choosing any database feature. The point is not to draw a perfect future schema. The point is to separate things that exist, facts about those things, links between them, rules that must remain true, and events that change what the organization knows. In this lesson, the working concepts are identity, entity, duplication, invariant. Keep the language ordinary: customer, appointment, source, document, status, owner, and time. If a model cannot be explained in those words, it is probably hiding a requirement rather than clarifying it.

## Minimal Concept Introduction

An entity is a thing the business talks about as a durable subject. An attribute is a fact about one entity at one moment. A relationship says that one entity is connected to another, and cardinality describes how many connections are expected or allowed. Identity is the answer to the question, "which one is this?" Duplication is not every repeated word; it is the same business fact stored in more than one place where the copies can disagree. An invariant is a rule the system should protect. A lifecycle event is something that happened, such as an order being placed or an appointment being canceled. A state transition is the movement from one named state to another. In Phase 0, these are paper-modeling ideas only. They are not yet database syntax.

## Worked Example

Consider a migration from legacy customer and order records into clearer target facts. A rough first pass might name the visible entities, then list attributes beside each one. For ecommerce, customer email belongs with the customer, product price belongs with the product until the order needs a remembered sale price, and order status belongs with the order. For scheduling, the appointment connects a provider and a client, while the appointment time is an attribute of that appointment rather than a free-floating fact. For document search, a document title belongs with the document, while a tag label belongs with the tag because several documents can carry the same tag. The same paper habit works across domains: name the thing, attach facts to the narrowest thing that owns them, name the relationship, then ask what could change over time.

## Diagnostic Questions

Ask these questions while reviewing a paper model. What are the candidate entities, and would domain experts recognize those nouns? Which attributes describe exactly one entity rather than a relationship or event? Where do we need identity because two similar records could otherwise be confused? Which relationships are one-to-one, one-to-many, or many-to-many in ordinary business language? What invariant would make a copied fact dangerous? What lifecycle event explains how the fact came to exist? In scheduling, for example, an appointment cancellation is not just a changed word; it is an event that changes the appointment state and may leave history that people later need to audit.

## Common Pitfalls

A common mistake is modeling screen labels instead of business facts. Another is using a convenient spreadsheet column as though it were the owner of truth. Learners also confuse legitimate repetition with duplication: two customers may share the same city, but a customer's current email copied onto many open support records can drift. Cardinality is often guessed from the first example rather than from the rule: one product in one order line is not the same as one product per order. Finally, paper models can skip lifecycle events because the current state looks enough. That shortcut fails when people ask how an order got refunded, why a provider became unavailable, or which imported row created a modern customer.

## Explain It Back

Explain the model without database words. Say which things exist, which facts describe them, which relationships connect them, and which rules should remain true after ordinary work happens. Then explain one event sequence in order. For modernization work, that might be import, validation, mapping, correction, promotion, or rollback depending on the scenario. If the explanation requires hand waving, write the ambiguity down instead of pretending it is solved. A good Phase 0 answer is modest and inspectable: it captures the facts that are known, flags the facts that are uncertain, and avoids turning syntax into a substitute for understanding.

## References and Further Reading

- [PostgreSQL Foundations doctrine](../../../../docs/doctrine.md) explains why the course treats database design as operational truth rather than syntax first.
- [Curriculum overview](../../../../curriculum/README.md) places this paper-modeling phase before SQL literacy.

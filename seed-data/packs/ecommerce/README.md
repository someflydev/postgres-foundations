# Ecommerce

## What this domain is

The ecommerce domain models a small store that sells catalog items and records customer orders. It is intentionally compact so learners can see each row and relationship before the same system becomes busier in later phases. The domain returns throughout the curriculum because order history, line-item grain, inventory pressure, and revenue reporting are familiar without requiring specialized business knowledge.

## Core entities

- Customers: people or accounts that place orders.
- Products: sellable catalog items with price and stock state.
- Orders: purchases placed by customers with operational status and money fields.
- Order items: per-product lines inside an order, introduced when joins and grain matter.

## Recurring scenarios

- Phase 0: model customers, products, orders, order items, statuses, and order
  lifecycle events on paper before SQL.
- Phase 1: retrieve recent orders and inspect product prices.
- Phase 2: join orders to line items and products.
- Phase 3: enforce non-negative quantities, non-negative totals, natural-key
  uniqueness, and reference-backed country and currency values.
- Phase 4b: use bounded product `tags text[]` as a good array fit and contrast
  it with a relational `price_history` table instead of a misleading range.
- Phase 5: compute running revenue with window functions.
- Phase 7: tune the hot order-history query.
- Phase 9: partition old orders by month.

## Non-goals

This pack does not model payments, tax law, shipment carriers, refunds, or fraud workflows. Those details are omitted unless a later lesson explicitly needs them to teach a PostgreSQL concept.

## Naming and schema overview

Large labs use the `ecommerce` schema. Small phase exercises may collapse these tables into `pgfound` when the lesson needs fewer moving parts. Tables: `customers`, `products`, `orders`, and `order_items`.

## Fixtures

- `fixtures/spreadsheet-legacy.csv`: a deliberately denormalized import sheet
  that mixes customers, orders, products, currencies, shipping status, and line
  items. Phase 3 uses it to practice refactoring spreadsheet-shaped data into
  customers, products, orders, and order_items while naming the constraints that
  prevent duplicate, conflicting, or impossible facts.

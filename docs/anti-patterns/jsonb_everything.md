# JSONB Everything

JSONB is useful when a value has genuinely variable shape, when the application often reads the document as a document, or when cold operational metadata does not justify a migration for every new key. JSONB is not a replacement for modeling.

The JSONB-everything anti-pattern appears when stable facts such as status, amount, tenant, email, timestamps, or frequently filtered categories are hidden inside a document. The result is weaker constraints, harder joins, text extraction in reports, ambiguous missing keys, and delayed migrations that become more expensive after production data drifts.

Prefer hot columns and cold JSONB. Put facts that are constrained, joined, sorted, grouped, or filtered every day into typed columns. Keep sparse, provider-specific, or rarely queried details in JSONB. When a JSONB key becomes hot, migrate it deliberately: add a column, backfill, review missing or misspelled keys, add constraints, update writers, then leave or remove the old JSONB key according to audit needs.

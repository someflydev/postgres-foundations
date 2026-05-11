# Constraints

- PostgreSQL 16.
- Confirmed appointments must use an exclusion constraint on
  `(professional_id WITH =, slot WITH &&)` where `slot` is a `tstzrange`.
- `btree_gist` may be used to support equality inside the GiST exclusion
  constraint.
- Availability templates use multirange values for recurring provider windows.
- Store appointment instants as `timestamptz`; render per provider timezone.
- The race where two patients book the same provider slot at the same time must
  be impossible at the database layer.
- No PostGIS yet; explain why geographic indexing is not justified.
- Full-text search on professional bios and specialties is optional but
  encouraged.
- Most submissions should decide not to partition appointments yet and explain
  the threshold that would change that decision.

# Solution

The proposed covering index includes too much payload. `INCLUDE` columns can help a narrow projection avoid heap fetches, but every included column makes the index larger and every order write more expensive. For the stated query, the useful payload is `order_number` and `total_amount`; status, currency, created_at, and updated_at are not needed.

The repair is to keep the key columns tied to search and order, then include only the projected payload. Verify whether PostgreSQL can use an `Index Only Scan`, and if it still performs heap fetches, explain the visibility-map condition instead of adding more columns.

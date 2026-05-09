# Solution

The missing invariant is that every imported customer must have one durable email and a name, and no two rows may claim the same email. Without this constraint, an incident could occur when a bulk import creates two customer identities for the same person and later order history splits across both rows.

A concrete repair is:

```sql
ALTER TABLE ecommerce.customers
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL;

ALTER TABLE ecommerce.customers
    ADD CONSTRAINT customers_email_unique UNIQUE (email);
```

Before applying it in a live migration, inspect duplicate emails, merge or quarantine conflicting rows, backfill missing names from the source system when possible, and then enforce the constraints. The rule belongs in PostgreSQL because admin scripts, loaders, and future services all write to the same table.

# Solution

The missing invariant is that customer, order, and product facts each need one owner. Without this constraint, an incident could occur when the same SKU has two product names in different order rows and a catalog update fixes only one copy.

A concrete repair is to split the sheet into keyed tables:

```sql
CREATE TABLE ecommerce.customers_normalized (
    id bigint generated always as identity PRIMARY KEY,
    email text NOT NULL UNIQUE,
    full_name text NOT NULL
);

CREATE TABLE ecommerce.products_normalized (
    id bigint generated always as identity PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    name text NOT NULL
);

CREATE TABLE ecommerce.orders_normalized (
    id bigint generated always as identity PRIMARY KEY,
    order_number text NOT NULL UNIQUE,
    customer_id bigint NOT NULL REFERENCES ecommerce.customers_normalized(id)
);
```

1NF removes repeating groups, 2NF keeps facts dependent on the whole key, and 3NF prevents non-key facts such as customer name from depending on another non-key value like email inside the order row.

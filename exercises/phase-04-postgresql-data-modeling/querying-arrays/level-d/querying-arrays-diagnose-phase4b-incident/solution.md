# Reference Solution

A strong answer explains that querying bounded tags directly from ecommerce.products is the good-fit shape, while using array operators to avoid modeling facts that need rows is the failure mode. It names the migration or query that makes PostgreSQL carry the truth directly, and it keeps indexing details as a later GIN or GiST pointer rather than the first fix.

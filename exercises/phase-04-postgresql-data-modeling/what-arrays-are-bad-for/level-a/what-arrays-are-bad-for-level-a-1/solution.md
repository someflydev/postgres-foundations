# Reference Solution

A strong answer explains that a child table for role grants when revocation and metadata matter is the good-fit shape, while packing lifecycle-bearing role facts into roles text[] is the failure mode. It names the migration or query that makes PostgreSQL carry the truth directly, and it keeps indexing details as a later GIN or GiST pointer rather than the first fix.

SELECT email, profile ->> 'locale' AS locale FROM ecommerce.customers ORDER BY email;

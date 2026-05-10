SELECT external_reference, count(*) FROM ecommerce.orders GROUP BY external_reference ORDER BY external_reference;

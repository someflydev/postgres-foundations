SELECT currency, count(DISTINCT customer_id) AS customers FROM ecommerce.orders GROUP BY currency ORDER BY currency;

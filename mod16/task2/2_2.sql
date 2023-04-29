SELECT full_name FROM customer
WHERE customer.customer_id NOT IN (SELECT customer_id FROM "order")
ORDER BY full_name;
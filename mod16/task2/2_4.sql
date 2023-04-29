SELECT order_no, customer_name FROM "order" o
LEFT JOIN
    (SELECT c.full_name as customer_name, c.customer_id as c_id
    FROM customer c
    WHERE manager_id IS NULL)
ON o.customer_id = c_id
WHERE customer_name IS NOT NULL
ORDER BY customer_name;
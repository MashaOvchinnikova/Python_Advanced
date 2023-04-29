SELECT order_no,
       m.full_name as manager_name,
       c.full_name as customer_name
    FROM "order" JOIN customer c on c.customer_id = "order".customer_id
        JOIN manager m on m.manager_id = "order".manager_id
    WHERE c.city != m.city;
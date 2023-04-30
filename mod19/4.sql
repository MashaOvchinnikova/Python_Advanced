-- Количество просроченных заданий для каждого класса
SELECT group_id, count(grade) as overdue_tasks_count
FROM (
    SELECT grade , group_id
    FROM assignments a
    JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
    WHERE ag.date > a.due_date
    )
GROUP BY group_id
ORDER BY overdue_tasks_count DESC;


-- Среднее количество просроченных заданий среди всех классов
SELECT round(avg(overdue_tasks_count)) as avg_overdue_tasks_count
FROM (
    SELECT count(grade) as overdue_tasks_count
    FROM (
        SELECT grade , group_id FROM assignments a
        JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
        WHERE ag.date > a.due_date
        )
    GROUP BY group_id
    ORDER BY overdue_tasks_count DESC
    );


-- Максимальное количество просроченных заданий среди всех классов
SELECT max(overdue_tasks_count) as max_overdue_tasks_count, group_id
FROM (
    SELECT group_id, count(grade) as overdue_tasks_count
    FROM (
        SELECT grade , group_id FROM assignments a
        JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
        WHERE ag.date > a.due_date
        )
    GROUP BY group_id
    ORDER BY overdue_tasks_count DESC
    );


-- Минимальное количество просроченных заданий среди всех классов
SELECT min(overdue_tasks_count) as min_overdue_tasks_count, group_id
FROM (
    SELECT group_id, count(grade) as overdue_tasks_count
    FROM (
        SELECT grade , group_id FROM assignments a
        JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
        WHERE ag.date > a.due_date
        )
    GROUP BY group_id
    ORDER BY overdue_tasks_count DESC
    )
--Общее количество учеников в каждой группе
SELECT group_id, count(*) as students_count FROM students
GROUP BY group_id;


--Средняя оценка по каждой группе
SELECT group_id, round(avg(grade), 2) as avg_grade FROM (
    SELECT group_id, grade
    FROM assignments a
    JOIN assignments_grades ag
        on a.assignment_id = ag.assignment_id
    )
GROUP BY group_id;


--Количество учеников, которые не сдали работы, по каждой группе
SELECT group_id, count(grade) as unreleased_tasks_count
FROM (
    SELECT grade , group_id
    FROM assignments a
    JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
    WHERE grade = 0
    )
GROUP BY group_id
ORDER BY unreleased_tasks_count DESC;


--Количество учеников, которые просрочили дедлайн, по каждой группе
SELECT group_id, count(grade) as overdue_tasks_count
FROM (
    SELECT grade , group_id
    FROM assignments a
    JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
    WHERE ag.date > a.due_date
    )
GROUP BY group_id
ORDER BY overdue_tasks_count DESC;


--Количество повторных попыток сдать работу по каждой группе
SELECT group_id, count(student) as repeated_attempts_count
FROM(
    SELECT t.student_id as student, group_id
    FROM students
    JOIN
        (SELECT student_id
         FROM assignments_grades
         GROUP BY student_id, assignment_id
         HAVING COUNT(student_id) > 1) as t
    ON students.student_id = t.student_id
    )
GROUP BY group_id

SELECT s.full_name as student_name, teachers_id, teacher_name
FROM students s
JOIN students_groups sg on s.group_id = sg.group_id
JOIN
(SELECT teachers_id, teacher_name, round(max(avg_grade), 2) as max_avg_grade
 FROM(
    SELECT t.full_name as teacher_name, t.teacher_id as teachers_id, avg(a_g.grade) as avg_grade
    FROM assignments_grades a_g
    JOIN assignments a on a_g.assignment_id = a.assignment_id
    JOIN teachers t on a.teacher_id = t.teacher_id
    GROUP BY teacher_name
    ORDER BY avg_grade))
ON sg.teacher_id=teachers_id
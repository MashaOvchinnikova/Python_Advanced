SELECT s.full_name as student_name, avg(a_g.grade) as avg_grade
FROM assignments_grades a_g
JOIN students s on s.student_id = a_g.student_id
GROUP BY student_name
ORDER BY avg_grade DESC
LIMIT 10
SELECT teacher_name, round(min(avg_grade), 2) as min_avg_grade FROM(
    SELECT t.full_name as teacher_name, avg(a_g.grade) as avg_grade
    FROM assignments_grades a_g
    JOIN assignments a on a_g.assignment_id = a.assignment_id
    JOIN teachers t on a.teacher_id = t.teacher_id
    GROUP BY teacher_name
    ORDER BY avg_grade);


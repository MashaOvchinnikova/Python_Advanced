SELECT round(avg(grade), 2) as avg_grade
FROM (
    SELECT grade
    FROM assignments a
    JOIN assignments_grades ag on a.assignment_id = ag.assignment_id
    WHERE assignment_text LIKE 'прочитать%'
       or assignment_text LIKE 'выучить%'
    )
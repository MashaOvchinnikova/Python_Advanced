import sqlite3

get_employee_with_increased_salary = """SELECT id, name, new_salary FROM (SELECT id, name, new_salary FROM(
        SELECT id, name, (salary + salary*0.1) as new_salary
        FROM table_effective_manager
        WHERE name=?))
WHERE new_salary <= (SELECT top_salary FROM (
        SELECT salary as top_salary
        FROM table_effective_manager
        WHERE name='Иван Совин'
                         ))"""


def ivan_sovin_the_most_effective(
        cur: sqlite3.Cursor,
        name: str,
):
    cur.execute(get_employee_with_increased_salary, (name, ))
    result = cur.fetchone()
    if result is None:
        cur.execute("""DELETE FROM table_effective_manager WHERE name = ?""", (name, ))
    else:
        new_salary = result[2]
        cur.execute("""UPDATE table_effective_manager 
        SET salary = ?
        WHERE name = ?""", (new_salary, name))


if __name__ == '__main__':
    with sqlite3.connect('hw.db') as conn:
        cursor = conn.cursor()
        emp_name = input('Введите имя сотрудника: ')
        ivan_sovin_the_most_effective(cursor, emp_name)

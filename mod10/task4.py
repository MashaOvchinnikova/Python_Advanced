import sqlite3


def question_one(curs):
    curs.execute("""SELECT COUNT(*) FROM salaries WHERE salary < 5000""")
    result = curs.fetchone()
    print(f'{result[0]} человек находятся за чертой бедности (получают меньше 5000)\n')


def question_two(curs):
    curs.execute("""SELECT AVG(salary) FROM salaries""")
    result = curs.fetchone()
    print(f'Средняя зарплата по острову: {result[0]}\n')


def question_three(curs):
    curs.execute("""SELECT AVG(salary)
    FROM (SELECT salary
          FROM salaries
          ORDER BY salary
          LIMIT 2 - (SELECT COUNT(*) FROM salaries) % 2
          OFFSET (SELECT (COUNT(*) - 1) / 2 FROM salaries))""")
    result = curs.fetchone()
    print(f'Медианная зарплата по острову: {result[0]}')


def question_four(curs):
    curs.execute("""SELECT 100 * round(CAST(T AS float)/CAST(K AS float),2) 
    FROM(
        SELECT SUM(other) as K, T
            FROM (
                SELECT salary as other
                FROM salaries
                ORDER BY salary DESC
                LIMIT (SELECT COUNT(salary) FROM salaries)
                OFFSET (SELECT COUNT(salary)*0.1 FROM salaries)
                )
        JOIN
        (SELECT SUM(TOP10) as T
            FROM (
                SELECT salary as TOP10
                FROM salaries
                ORDER BY salary DESC
                LIMIT (SELECT COUNT(salary)*0.1 FROM salaries)
                )
        )
    )""")
    result = curs.fetchone()
    print(f'Число социального неравенства в процентах: {result[0]}')


if __name__ == '__main__':
    with sqlite3.connect('db/hw_4_database.db') as conn:
        cursor = conn.cursor()
        question_one(cursor)
        question_two(cursor)
        question_three(cursor)
        question_four(cursor)


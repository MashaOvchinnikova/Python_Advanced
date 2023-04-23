import sqlite3


def question_one(curs):
    curs.execute("""SELECT COUNT(*) FROM table_1""")
    table_one_count = curs.fetchone()
    print(f'Количество строк в первой таблице: {table_one_count[0]}')

    curs.execute("""SELECT COUNT(*) FROM table_2""")
    table_two_count = curs.fetchone()
    print(f'Количество строк во второй таблице: {table_two_count[0]}')

    curs.execute("""SELECT COUNT(*) FROM table_3""")
    table_three_count = curs.fetchone()
    print(f'Количество строк в третьей таблице: {table_three_count[0]}\n')


def question_two(curs):
    curs.execute("""SELECT COUNT(DISTINCT value) FROM table_1""")
    result = curs.fetchone()
    print(f'Количество уникальных записей в первой таблице: {result[0]}\n')


def question_three(curs):
    curs.execute(""" SELECT table_1.value 
    FROM table_1 
    JOIN table_2 
    ON table_2.value = table_1.value 
    GROUP BY table_1.value""")
    result = curs.fetchall()
    print(f'Во второй таблице встречается {len(result)} записей из первой таблицы:')
    for row in result:
        print(row)


def question_four(curs):
    curs.execute("""SELECT table_2.value 
    FROM table_2
    INTERSECT 
    SELECT table_3.value 
    FROM table_3 
    INTERSECT 
    SELECT table_1.value 
    FROM table_1""")
    result = curs.fetchall()
    print(f'\nИ в третьей и во второй таблице встречается {len(result)} записей из первой таблицы:')
    for row in result:
        print(row)


if __name__ == '__main__':
    with sqlite3.connect('db/hw_3_database.db') as conn:
        cursor = conn.cursor()
        question_one(cursor)
        question_two(cursor)
        question_three(cursor)
        question_four(cursor)

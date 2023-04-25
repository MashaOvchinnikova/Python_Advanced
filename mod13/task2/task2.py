import sqlite3
import csv

delete_wrong_fees_sql_request = """
DELETE 
FROM table_fees
WHERE table_fees.timestamp=? AND truck_number=?"""


def delete_wrong_fees(
        cur: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            time, truck_number = row[0], row[1]
            cur.execute(delete_wrong_fees_sql_request, (time, truck_number))


if __name__ == '__main__':
    with sqlite3.connect('../hw.db') as conn:
        cursor = conn.cursor()

        # В my_wrong_fees_list хранятся 10 дат и номеров автомобилей ошибочных штрафов,
        # взятых из первых 10 записей таблицы table_fees, поэтому после удаления в
        # таблице table_fees не будет первых 10 записей
        delete_wrong_fees(cursor, "my_wrong_fees_list.csv")


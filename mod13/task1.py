import sqlite3


check_count_of_wrong_temperature_sql = """
SELECT COUNT(*)
FROM table_truck_with_vaccine
WHERE truck_number = ?
AND temperature_in_celsius NOT BETWEEN 16 and 20"""


def check_if_vaccine_has_spoiled(
        cur: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cur.execute(check_count_of_wrong_temperature_sql, (truck_number, ))
    result, *_ = cur.fetchone()
    if result >= 3:
        return True
    return False


if __name__ == '__main__':
    with sqlite3.connect('hw.db') as conn:
        cursor = conn.cursor()
        # truck_num = input('Введите номер грузовика: ')
        truck_num = 'у043вт13'
        if check_if_vaccine_has_spoiled(cursor, truck_num):
            print(f'В грузовике с номером {truck_num} был нарушен температурный режим')
        else:
            print('fС вакциной все ок')


import datetime
import sqlite3


def log_bird(
        cur: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    cur.execute("""
    INSERT INTO table_birds (bird_name, date_time) 
    VALUES (?,?)""", (bird_name, date_time))


def check_if_such_bird_already_seen(cur: sqlite3.Cursor, bird_name: str) -> bool:
    cur.execute("""
    SELECT EXISTS (SELECT * FROM table_birds 
    WHERE bird_name=?)""", (bird_name, ))
    result, *_ = cur.fetchone()
    if result == 1:
        return True
    return False


if __name__ == "__main__":

    name = input("Пожалуйста введите имя птицы\n> ")
    right_now = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("hw.db") as connection:
        cursor = connection.cursor()
        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        log_bird(cursor, name, right_now)



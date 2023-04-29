import sqlite3

with open('create_schema.sql', 'r') as sql_file:
    sql_script: str = sql_file.read()

with sqlite3.connect('hw_database.db') as connection:
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()





import sqlite3

table_user = '''CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(30),
  last_name VARCHAR(30),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);'''


def create_db(file: str) -> None:
    # читаем файл со скриптом для создания БД
    with open(file, 'r') as file:
        sql = file.read()

    # создаем соединение с БД (если файла с БД нет, он будет создан)
    with sqlite3.connect('DB/chef_app.db') as con:
        cur = con.cursor()
        # выполняем скрипт из файла, который создаст таблицы в БД
        cur.executescript(sql)


if __name__ == "__main__":
    file = 'DB/sql_users.sql'
    file_reciepts = 'DB/sql_reciept.sql'

    create_db(file_reciepts)

import sqlite3
from sqlite3 import Error

db_path = 'DB/chef_app.db'
def add_users_to_db(user_id, user_name, last_name):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()

        sql_to_user = """INSERT INTO users(id, name, last_name) VALUES (?, ?, ?)"""

        try:
            cur.execute(sql_to_user, (user_id, user_name, last_name))
            con.commit()

        except Error as err:
            print(err)
        finally:
            cur.close()

def save_reciepts(meal_id, title, instructions, image):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()

        sql_to_receipt = """INSERT INTO receipts(id, title, instructions, image) VALUES (?, ?, ?, ?)"""

        try:
            cur.execute(sql_to_receipt, (meal_id, title, instructions, image))
            con.commit()

        except Error as err:
            print(err)
        finally:
            cur.close()

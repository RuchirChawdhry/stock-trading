import sqlite3, os
import pandas as pd
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)
db = sqlite3.connect("data.db")


def create_tables():  # Creating sqlite database with tables: users, stocks
    with sqlite3.connect("data.db") as db:
        c = db.cursor()

        c.execute('''
                       CREATE TABLE IF NOT EXISTS users
                       (userID INTEGER PRIMARY KEY AUTOINCREMENT,
                       username NOT NULL UNIQUE,
                       password NOT NULL,
                       bankAccount DEFAULT 100000);''')

        c.execute('''
                       CREATE TABLE IF NOT EXISTS stocks
                       (orderID INTEGER PRIMARY KEY AUTOINCREMENT,
                       username NOT NULL,
                       stockSymbol NOT NULL,
                       orderType NOT NULL,
                       orderTime DATETIME NOT NULL,
                       price NOT NULL,
                       numShares NOT NULL);'''
                  )  # OrderType is either b (buy) or s (sell)
        # OrderUserID is the User ID who placed
        # the order

    db.commit()


def seed_users():
    try:
        seed_users = ["user", "user1", "user2"]
        seed_passwords = ["user", "password", "password"]
        seed_tup = list(zip(seed_users, seed_passwords))
        df = pd.DataFrame(seed_tup, columns=["username", "password"])
        df.to_sql("users", db, if_exists="append", index=False)
    except:
        pass


# def stock_table_update():
#     with sqlite3.connect("data.db") as db:
#         c = db.cursor()
#
#
#         cursor.execute('''UPDATE stocks SET stockSymbol WHERE username = ?''')

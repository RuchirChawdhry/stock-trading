import sqlite3, os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)

# Creating sqlite database with tables: users, stocks
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
                   orderUserID INTEGER NOT NULL,
                   stockSymbol NOT NULL,
                   orderType NOT NULL,
                   orderTime DATETIME NOT NULL,
                   price NOT NULL,
                   numShares NOT NULL,
                   bankAccount DEFAULT 100000);''') # OrderType is either b (buy) or s (sell)
                                                    # OrderUserID is the User ID who placed
                                                    # the order
db.commit()

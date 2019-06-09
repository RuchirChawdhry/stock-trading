import sqlite3
import time
import os
import json
import pyfiglet
import pandas as pd
from urllib.request import urlopen

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)


def login():
    while True:
        current_user = []
        username = input("Enter Username:")
        password = input("Enter Password:")
        with sqlite3.connect('data.db') as db:
            cursor = db.cursor()
        find_user = ("SELECT * from users WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Welcome, " + i[1] + "!\n")
            login.current_user = list(results[0])
            return current_user
            # return ("exit")

        else:
            print("Username and/or password not found. ")
            again = input("Do you want to try again? (y/n): ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                # return("exit")
                break


def register():
    found = 0
    while found == 0:
        username = input("Enter a username: ")
        with sqlite3.connect("data.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM users WHERE username = ?")
        cursor.execute(findUser, [(username)])

        if cursor.fetchall():
            print("Username already taken. Please try again.")
        else:
            found = 1
        password = input("Please enter your password: ")
        password_re = input("Please re-enter your password: ")
        while password != password_re:
            print("Your password did not match. Please try again.")
            password = input("Please enter your password: ")
            password_re = input("Please re-enter your password: ")
        insertData = '''INSERT INTO users(username, password)
            VALUES(?,?)'''

        cursor.execute(insertData, [username, password])
        db.commit()


def heading():
    heading_ = pyfiglet.figlet_format("Welcome Stock Trader!", font="starwars")
    print(heading_ + '\n')
    sub_heading = pyfiglet.figlet_format("Select option:", font="bubble")
    print(heading)
    print(sub_heading)


def initial_menu():
    # while True:
    option_1 = "[1] --- > Login"
    option_2 = "[2] --- > Register"
    option_3 = "[3] --- > Search by Company Name or Symbol (w/o Logging-in)"
    # //TODO: If users logs out as remove all elements in the current_user list.
    print(option_1)
    print(option_2)
    print(option_3)
    print("\n")


def loggedin_menu():
    option_login_1 = "[1] --- >> Search by Company Name or Symbol"
    option_login_2 = "[2] --- >> Get Latest Stock Quote"
    option_login_3 = "[3] --- >> View Your Portfolio"
    option_login_4 = "[4] --- >> Buy Stocks"
    option_login_5 = "[5] --- >> Sell Stocks"
    option_login_6 = "[6] --- >> Logout as: " + str(login.current_user)
    print(option_login_1)
    print(option_login_2)
    print(option_login_3)
    print(option_login_4)
    print(option_login_5)
    print(option_login_6)
    print("\n")


def menu():
    initial = True
    loggedin = True
    while initial == True:
        initial_menu()
        choice = input("Enter Menu Number:")
        # choice = int(choice)
        # map the options to functions
        menu_funcs = {'1': login, '2': register, '3': company_search}
        # menu()
        # if choice == 'q':
        #     return # exit

        if choice in menu_funcs:
            menu_funcs[choice]()  # call the function
        if choice == '1':
            initial == False

            while loggedin == True:
                loggedin == True
                loggedin_menu()

                choice_ = input("Enter Menu Number:  ")
                menu_funcs_loggedin = {
                    '1': company_search,
                    '2': get_quote,
                    '3': view_portfolio,
                    '4': buy_stock,
                    '5': sell_stock,
                    '6': logout
                }
                if choice_ in menu_funcs_loggedin:
                    menu_funcs_loggedin[choice_]()
                if choice_ == '6':
                    loggedin == False
                    initial == True
                    break
                else:
                    print(
                        "That is not a valid choice. You can only choose from the menu."
                    )

        else:
            print(
                "That is not a valid choice. You can only choose from the menu."
            )


def company_search():
    search = input("Enter company name or symbol to search: ")
    url = 'http://dev.markitondemand.com/Api/v2/Lookup/json?input=' + search
    data = pd.read_json(url)
    if data.empty:
        print('No results found')
    else:
        print(data)


def get_quote():
    search_quote = input("Enter stock symbol: ")
    url = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + search_quote
    df = pd.DataFrame([requests.get(url).json()])
    display(df)


def leaderboard():
    pass


def buy_stock():
    buy_quote = input("Enter exact stock symbol you want to buy: ")
    num_shares = input("Number of shares you want to buy of " +
                       buy_quote.upper() + "? ")
    url = urlopen(
        'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' +
        buy_quote)
    obj = json.load(url)
    stock_price = obj["LastPrice"]
    # //TODO: Add import to database for buy_stock (UserID, stock_symbol, time_stamp, number_shares)
    # //TODO: Immediately deduct the INR from bank account the moment the user buys a stock.


def sell_stock():
    sell_quote = input("Enter exact stock symbol you want to sell: ")
    num_shares_sold = input("Number of shares you want to sell of " +
                            sell_quote.upper() + "? ")
    url = urlopen(
        'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' +
        buy_quote)
    obj = json.load(url)
    stock_price = obj["LastPrice"]
    # //TODO: Immediately add to bank account the moment the user sells a stock.
    # //TODO: Add import to database for sell_stock (UserID, stock_symbol, time_stamp, number_shares)


def view_portfolio():
    pass


def logout():
    # del login.current_user
    login.current_user.clear()


if __name__ == "__main__":
    heading()
    menu()

from cs50 import SQL
import time


# Globals
db = SQL("sqlite:///atm.db")

# User authentication, return 0 to login, return 1 to reject
def user_authentication(user, password):
    rows = db.execute("SELECT * FROM accounts WHERE account_no = ? AND pin = ?", user, password)
    if len(rows) == 1:
        return 0
    else:
        return 1

# Returns user id when called
def user(user):
    user_id = db.execute("SELECT id FROM accounts WHERE account_no = ?", user)
    return user_id


# Executes deposit and returns 0 if successful
def deposit(user_id, deposit):
    try:
        db.execute("INSERT INTO transactions (user_id, amount, date) VALUES(?, ?, julianday('now'))", user_id, deposit)
        return 0
    except:
        return 1


# Executes withdraw and returns 0 if successful
def withdraw(user_id, withdraw):
    try:
        withdraw = withdraw * -1
        db.execute("INSERT INTO transactions (user_id, amount, date) VALUES(?, ?, julianday('now'))", user_id, withdraw)
        return 0
    except:
        return 1

    
# Queries the user's balance
def balance(user_id):
    balance = db.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ?", user_id)
    balance = round(balance[0]["SUM(amount)"],2)
    return balance


# Queries the user's statement
def statement(user_id):
    statement = db.execute("SELECT date(date), amount FROM transactions WHERE user_id = ? ORDER BY date(date) DESC", user_id)
    return statement

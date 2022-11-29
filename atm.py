import time
import os
import bank

########## Globals ############

USER_ID = ""
width = 60

########## Navigation Functions ############

# Login menu with account and pin validation done in bank.py
def login():
    os.system('clear')
    while True:
        banner("Please Login to Your Account")
        user = input(f'\n{"Enter Account Number: ":<22}')
        password = input(f'{"Enter Pin Number: ":<22}')
        verify = bank.user_authentication(user, password)
        if verify == 0:
            loading_bar('Logging in')
            user_id = bank.user(user)
            global USER_ID
            USER_ID = user_id[0]["id"]
            menu()
            break
        else:
            print("Invalid Account or PIN Number. Please try again")

# Main menu for user to navigate different transactions 
def menu():
    os.system('clear')
    banner(" Welcome to Your Account ")
    print('    1 - Make Withdraw\n\n    2 - Make Deposit\n\n    3 - Check Balance\n\n    4 - View Transactions\n\n    5 - Logout\n\n    6 - Exit Application\n\n')
    selection = int(input("What would you like to do? "))
    loading_bar('Loading')
    if selection == 1:
        withdraw()
        return_menu()
    elif selection == 2:
        deposit()
    elif selection == 3:
        balance()
        return_menu()
    elif selection == 4:
        statement()
        return_menu()
    elif selection == 5:
        login()
    elif selection == 6:
        os.system('clear')
        exit
        return 0

# Return to menu if user inputs 'y'
def return_menu():
    while True:
        print()
        nav = input("Would you like to make another transaction? (Y/N) ")
        if nav.lower() == "y":
            menu()
            break
        elif nav.lower() == "n":
            os.system('clear')
            exit
            break
        

########## Transactions ############


# Deposit function
def deposit():
    os.system('clear')
    banner('Make Deposit')
    deposit = float(input("How much would you like to deposit? $"))
    status = bank.deposit(USER_ID, deposit)
    loading_bar('Loading')
    if status != 0:
        print("\n    Deposit Successful!")
        return_menu()
    else:
        print("There was an unexpected error. Please try again later!")
        menu()
    

# Withdraw function
def withdraw():
    os.system('clear')
    banner('Make Withdraw')
    withdraw = float(input("How much would you like to withdraw? $ "))
    balance = bank.balance(USER_ID)
    if withdraw <= balance:
        status = bank.withdraw(USER_ID, withdraw)
        if status == 0:
            print("Your withdraw was successful!")
        else:
            print(f"There was an issue with your transaction. Please try again later. \nError: {status}")
    else:
        print('You do not have enough funds.')    


# Balance function
def balance():
    os.system('clear')
    banner('Your Balance')
    print()
    balance = bank.balance(USER_ID)
    print(f'Your balance is: $ {balance}')
    print()


# Statement function
def statement():
    os.system('clear')
    banner('Your Transactions')
    balance = bank.balance(USER_ID)
    statement = bank.statement(USER_ID)
    col = int((width - 3) / 3)
    print(f'Your balance is: $ {balance}\n')
    print(f'|{"Date":^{col}}|{"Description":^{col - 1}}|{"Amount":^{col}}|')
    print("-" * width)
    for row in statement:
        date = row["date(date)"]
        amount = round(row["amount"], 2)
        if amount < 0:
            description = "Withdraw"
        elif amount > 0:
            description = "Deposit"
        print(f'|{date:^{col}}|{description:^{col - 1}}| $ {amount:>{col - 3},.2f}|')   


########## Interface ############

# Simulates a loading bar with input argument for message to be displayed
def loading_bar(message):
    print()
    for i in range(21):
        print(' ' + message + ' [' + '#' * i + '_' * (20 - i) + ']', end='\r')
        time.sleep(0.02)
    print()


# Banner function with input argument for message to be displayed
def banner(message):
    col = int(width / 2)
    marg1 = int(col / 2)
    marg2 = int(width - col - marg1)
    marg = int(width / 5)
    margin = "#" * marg
    print(f'#' * width)
    print(f'{margin:<{marg1}}{message:^{col}}{margin:>{marg2}}')
    print(f'#' * width)
    print()


login()
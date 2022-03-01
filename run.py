import gspread # Importing to open and edit pizza ordering spreadsheet
from google.oauth2.service_account import Credentials
from tabulate import tabulate # Importing tabulate to present data to the user clearly
import re # Importing re module for validating mobile phone number


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vv_pizzas')


def get_customer_info():
    """
    Welcome customer and request key customer information for the order
    """
    print("Thank you for choosing Vera's Vegan Pizzas!\n")
    print("Please follow the steps to place your order,")
    print("and collect 20 minutes later.\n")

    """
    Request and validate customers name
    """
    while True:
        name = input("Please provide your name:\n").lower()
        if name.isalpha(): # Validates the customer as entered a character based name
            break
        else:
            print("Invalid name, please try again")  
        return name  
    print(f"Hi {name.capitalize()}\n")
    
    """
    Request and validate customers mobile phone number 
    """
    def validate_mobile(telnum):
        numPattern = re.compile("(0)?[0-9]{11}") # Validates number to begin with 0 and be 11 digits only
        return numPattern.match(telnum)
    
    while True:
        telnum = input("Please provide a mobile contact number:\n")
        if (validate_mobile(telnum)):
            break
        else:
            print(f"Invalid number. Exactly 11 digits required, starting with 0, please try again")
        return telnum    
    print(f"Thanks {name.capitalize()}, we will use {telnum} to contact you if there's any issue with your order.\n")


def get_topping():
    """
    Present the customer with the choice of toppings and request a choice of 1-4
    """
    print("Here are todays choices of toppings, Which would you like?")
    print("[1] Margherita")
    print("[2] Romana")
    print("[3] Diavolo")
    print("[4] Forza\n")

    """
    Request and validate the customers choice is between 1-4
    """
    while True:
        try:
            topping = int(input("Please choose a topping by typing the corresponding number and clicking enter:\n"))
        except ValueError:
            print("Invalid choice, please enter a number")  
            continue
        if topping in range(1, 5, 1): # change to a data dictionary so the return print message is a string value
            print(f"Thanks for choosing a {topping}")
        else:
            print("Invalid choice, please try again") 
            continue
        return topping
         

def get_size():
    """
    Present the customer with the choice of sizes and request a choice S, M, L
    """
    print("Which size of pizza would you like?")
    print('[S] Small 7"')
    print('[M] Medium 10"')
    print('[L] Large 14"')

    """
    Request and validate the customers choice is either S, M or L
    """
    while True:
        size = input("Please choose a size by entering the corresponding letter and clicking enter:\n")
        if size == ('S').lower():
            print(f"Thanks for choosing Small")
        elif size == ('M').lower():
            print(f"Thanks for choosing Medium")
        elif size == ('L').lower():
            print(f"Thanks for choosing Large")
        else:
            print("Invalid choice, please enter either S, M or L")
            continue
        return size





get_customer_info()
get_topping()
get_size()
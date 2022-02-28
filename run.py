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
        name_str = input("Please provide your name:\n").lower()
        if name_str.isalpha(): # Validates the customer as entered a character based name
            break
        else:
            print("Invalid name, please try again")    
    print(f"Hi {name_str.capitalize()}\n")
    
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
    print(f"Thanks {name_str.capitalize()}, we will use {telnum} to contact you if there's any issue with your order.\n")


def get_topping():
    """
    Present the customer with the choice of toppings and request a choice of 1-4
    """
    print("Here are todays choices of toppings...")
    print("[1] Margherita")
    print("[2] Romana")
    print("[3] Diavolo")
    print("[4] Forza\n")

    """
    Validate the customers choice is between 1-4
    """
    topping = int(input("Please choose a topping by typing the number and clicking enter:\n"))
# sort out validation for topping selection - think there is an issue with the [1] format so maybve move to a data dictionary or tabulate for the choice.
    def validate_topping(topping):
        numTopping = re.compile("[1-4]{1}") # Validates the choice is between 1-4
        return numTopping.match(topping)
# think the IF statement is ok just need to validate the selection 
    if (validate_topping(topping)):
        print(f"Thanks for choosing a {topping} {get_customer_info().name_str.capitalize()}\n")
    else:
        print(f"Invalid choice, please try again")    

    
get_customer_info()
get_topping()
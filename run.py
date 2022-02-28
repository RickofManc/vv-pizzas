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
        if name_str.isalpha(): # Validate the customer as entered a character based name
            break
        else :
            print("Invalid name, please try again")    
    print(f"Hi {name_str.capitalize()} \n")
    
    """
    Request and validate customers mobile phone number 
    """
    telnum = input("Please provide a mobile contact number:\n")
    def validate_mobile(telnum):
        numPattern = re.compile("(0)?[0-9]{11}") # Validate number to begin with 0 and be 11 digits only
        return numPattern.match(telnum)

    if (validate_mobile(telnum)):
        print(f"Thanks {name_str.capitalize()}, we will use {telnum} to contact you if there's an issue with your order.\n")
    else :
        print(f"Exactly 11 digits required, starting with 0, please try again")


get_customer_info()
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

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
    Request customers name and telephone number for the order
    """
    print("Thank you for choosing Vera's Vegan Pizzas!\n")
    print("Please follow the steps to place your order,")
    print("and collect 20 minutes later.\n")

    name_str = input("Please provide your name:\n")
    print(f"Hi {name_str} \n")
    
    tel_str = input("Please provide a contact number:\n")
    print(f"Thanks {name_str}, we will use {tel_str} to contact you if there's an issue with your order\n")

get_customer_info()


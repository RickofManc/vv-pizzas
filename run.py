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

class Customer:
    """
    Customer data class
    """
    def get_customer_data():
        """
        Request and validate customers name and telephone number
        """
        while True:
            name = input(f"Please provide your name:\n").lower()
            if name.isalpha(): # Validates the customer as entered a character based name
                break
            else:
                print(f"Invalid name, please try again\n")  
            return name  
        print(f"Hi {name.capitalize()}\n")
            
        """
        Request and validate customers mobile phone number 
        """
        def validate_mobile(telnum):
            numPattern = re.compile("(0)?[0-9]{11}") # Validates number to begin with 0 and be 11 digits only
            return numPattern.match(telnum)
            
        while True:
            telnum = input(f"Please provide a mobile contact number:\n")
            if (validate_mobile(telnum)):
                break
            else:
                print(f"Invalid number. Exactly 11 digits required, starting with 0, please try again\n")
            return telnum    
        print(f"Thanks {name.capitalize()}, we will use {telnum} to contact you if there's any issue with your order.\n")

class Topping:
    """
    Pizza topping class
    """
    def get_topping():
        """
        Present the customer with the choice of toppings and request a choice of 1-4
        """
        print("Here are todays choices of toppings, which would you like?")
        print("[1] Margherita")
        print("[2] Romana")
        print("[3] Diavolo")
        print("[4] Forza\n")

        """
        Request and validate the customers choice is between 1-4
        """
        while True:
            try:
                topping = int(input(f"Please choose a topping by typing the corresponding number and clicking enter:\n"))
            except ValueError:
                print(f"Invalid choice, please enter a number\n")  
                continue
            if topping in range(1, 5, 1): # change to a data dictionary so the return print message is a string value
                print(f"Thanks for choosing a {topping}\n")
            else:
                print(f"Invalid choice, please try again\n") 
                continue
            return topping
         
class Size:
    """
    Pizza topping size
    """
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
            size = input(f"Please choose a size by entering the corresponding letter and clicking enter:\n")
            if size == ('S').lower():
                print(f"Thanks for choosing Small\n")
            elif size == ('M').lower():
                print(f"Thanks for choosing Medium\n")
            elif size == ('L').lower():
                print(f"Thanks for choosing Large\n")
            else:
                print(f"Invalid choice, please enter either S, M or L\n")
                continue
            return size


#def confirm_order():
    """
    Collate the choices made by the customer
    Present the choices to the customer
    Ask the customer to either place the order or,
    add more items to the order
    """

    #print(f"Thanks (get_customer_data.({name.capitalize()})))


#def update_order_worksheet(custOrder):
    #print(f"Thanks. Sending your order to Vera in the kitchen...\n")
    #orders_worksheet = SHEET.worksheet("Orders")
    #orders_worksheet.append_row(custOrder)
    #print(f"Your order has been received, please come and collect in 20 minutes.\n See you soon!\n")


def main():
    """
    Run all program functions
    """
    custData = Customer.get_customer_data()
    custTopping = Topping.get_topping()
    custSize = Size.get_size()
    #custOrder = confirm_order()
    #update_order_worksheet(custOrder)


print("Thank you for choosing Vera's Vegan Pizzas!\n")
print("Please follow the steps to place your order,")
print("and collect 20 minutes later.\n")
main()
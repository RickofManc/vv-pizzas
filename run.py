import re  # Importing re module for validating mobile phone number
import gspread  # Importing to open and edit pizza ordering spreadsheet
from google.oauth2.service_account import Credentials
from tabulate import tabulate  # Importing to present data to the user clearly


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vv_pizzas')


def get_customer_data():
    """
    Request and validate customers name and telephone number
    """
    while True:
        name = input("Please provide your name:\n").lower()
        if name.isalpha():  # Validates the customer is characters only
            break
        else:
            print("Invalid name, please try again\n")
        return name
    print(f"Hi {name.capitalize()}\n")

    def validate_mobile(telnum):
        """
        Request and validate customers mobile phone number.
        Number must begin with 0 and be 11 digits.
        """
        num_pattern = re.compile("(0)?[0-9]{11}")
        return num_pattern.match(telnum)

    while True:
        telnum = (input("Please provide a mobile contact number:\n"))
        if validate_mobile(telnum):
            break
        else:
            print("Invalid number. 11 digits required, starting with 0, please try again\n")
        return telnum
    print(f"Thanks {name.capitalize()}, we will use {telnum} to contact you if there's any issue with your order.\n")


def get_topping():
    """
    Present the customer with the choice of toppings,
    and request a choice of 1-4
    """
    print("Here are todays choices of toppings, which would you like?")
    print("[1] Margherita")
    print("[2] Romana")
    print("[3] Diavolo")
    print("[4] Forza\n")

    # Request and validate the customers choice is between 1-4
    while True:
        try:
            topping = int(input("Please choose a topping by typing the corresponding number and clicking enter:\n"))
        except ValueError:
            print("Invalid choice, please enter a number\n")
            continue
        # change to a data dict to return print msg is a string value
        if topping in range(1, 5, 1):  
            print(f"Thanks for choosing a {topping}\n")
        else:
            print("Invalid choice, please try again\n")
            continue
        return topping


def get_size():
    """
    Present the customer with the choice of sizes,
    and request a choice S, M, L
    """
    print("Which size of pizza would you like?")
    print('[S] Small 7"')
    print('[M] Medium 10"')
    print('[L] Large 14\n"')

    #  Request and validate the customers choice is either S, M or L
    while True:
        size = input("Please choose a size by entering the corresponding letter and clicking enter:\n")
        if size == ('S').lower():
            print("Thanks for choosing Small\n")
        elif size == ('M').lower():
            print("Thanks for choosing Medium\n")
        elif size == ('L').lower():
            print("Thanks for choosing Large\n")
        else:
            print("Invalid choice, please enter either S, M or L\n")
            continue
        return size


def confirm_order():
    """
    Confirm the order back to the customer
    ask the customer to proceed Y/N
    provide an opportunity to order more items
    """
    topping = get_topping()
    size = get_size()

    print(f"Thanks, to confirm, you have ordered a {size} {topping}")
   
    while True:
        # need to code how to get the values from the other classes - do we pass them into the main() function?
        cust_order = input("Is this ready to be sent to the kitchen? Y/N:\n")
        if cust_order == ('Y').lower():
            print("Thanks. Sending your order to Vera in the kitchen...\n")
            orders_worksheet = SHEET.worksheet("Orders")
            orders_worksheet.append_row(cust_order)
            print("Your order has been received, please come and collect in 20 minutes.\n See you soon!\n")
        elif cust_order == ('N').lower():
            more_items = input("That's ok. Would you like to order more items? Y/N\n")
            if more_items == ('Y').lower():
                print("I need to code how to add more items")
            elif more_items == ('N').lower():
                amend_order = input("Would you like to amend this order? Y/N\n")
                if amend_order == ('Y').lower():
                    print("I need to code how to amend the order")
                elif amend_order == ('N').lower():
                    confirm_order()
                else:
                    print("Invalid choice, please enter either Y or N\n")
                    continue
            else:
                print("Invalid choice, please enter either Y or N\n")
                continue
        else:
            print("Invalid choice, please enter either Y or N\n")
            continue
        return f'{"Thanks Customer.name() for ordering a Size.size() Topping.topping()"}'


def main():
    """
    Run all program functions
    """
    get_customer_data()
    confirm_order()


print("Thank you for choosing Vera's Vegan Pizzas!\n")
print("Please follow the steps to place your order,")
print("and collect 20 minutes later.\n")
main()
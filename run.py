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


def get_customer_name():
    """
    Request and validate customers name
    """
    while True:
        name = input("Please provide your name:\n").lower()
        if name.isalpha():  # Validates the customer is characters only
            print(f"Hi {name.capitalize()}\n")
        else:
            print("Invalid name, please try again\n")
            continue
        return name


def get_customer_number():
    """
    Request and validate customers telephone number
    """
    def validate_mobile(telnum):
        """
        Validates customers mobile phone number.
        Number must begin with 0 and be 11 digits.
        """
        num_pattern = re.compile("(0)?[0-9]{11}")
        return num_pattern.match(telnum)
    # Request telephone number, break if valid or provide error message
    while True:
        telnum = (input("Please provide a mobile contact number:\n"))
        if validate_mobile(telnum):
            print(f"Thanks, we will use {telnum} to contact you if there's any issue with your order.\n")
        else:
            print("Invalid number. 11 digits required, starting with 0, please try again\n")
            continue
        return telnum


def get_pizza():
    """
    Present the customer with the choice of pizza,
    and request a choice of 1-4
    """
    #  Data to populate the table of pizza choices
    pizza_table = [
        [1, "Margherita", "Vegan mozzarella and tomato."],
        [2, "Giardiniera", "Artichoke, mushrooms, red onion, black olives"],
        [3, "Diavolo", "Smoky jackfruits, green peppers, chilli oil."],
        [4, "Forza", "Chilli Quorn™, mixed peppers, sweet chilli peppers."]
        ]
    print("Here are todays pizzas, which would you like?\n")
    print(tabulate(
        pizza_table,
        headers=["Item", "Pizza", "Topping"],
        tablefmt="psql"),
        "\n"
        )
    # Request and validate the customers choice is between 1-4
    while True:
        pizza = int(input("Please choose a pizza by typing the corresponding number and clicking enter:\n"))
        if pizza == 1:
            print("Yummy! a Margherita!\n")
            return 'Margherita'
        elif pizza == 2:
            print("Yummy! a Giardiniera!\n")
            return 'Giardiniera'
        elif pizza == 3:
            print("Yummy! a Diavolo!\n")
            return 'Diavolo'
        elif pizza == 4:
            print("Yummy! a Forza!\n")
            return 'Forza'
        else:
            print("Invalid choice, please enter a number between 1-4\n")
            continue


def get_size():
    """
    Present the customer with the choice of sizes,
    and request a choice S, M, L
    """
    #  Tabular data to inform the table of choices for the user
    sizes_table = [
        ["S", "Small", "8 Inches"],
        ["M", "Medium", "10 Inches"],
        ["L", "Large", "14 Inches"]
        ]
    print("Which size of pizza would you like?\n")
    print(tabulate(
        sizes_table,
        headers=["Item", "Name", "Size"],
        tablefmt="psql"),
        "\n"
        )
    #  Request and validate the customers choice is either S, M or L
    while True:
        size = input("Please choose a size by entering the corresponding letter and clicking enter:\n")
        if size == ('S').lower():
            print("Thanks for choosing Small\n")
            return 'Small'
        elif size == ('M').lower():
            print("Thanks for choosing Medium\n")
            return 'Medium'
        elif size == ('L').lower():
            print("Thanks for choosing Large\n")
            return 'Large'
        else:
            print("Invalid choice, please enter either S, M or L\n")
            continue


def confirm_order():
    """
    Confirm the order back to the customer
    ask the customer to proceed Y/N
    provide an opportunity to order more items
    """
    name = get_customer_name()
    pizza = get_pizza()
    size = get_size()

    print(f"Thanks {name.capitalize()}, you are ordering a {size} {pizza}\n")

    while True:
        # need to code how to get the values from the other classes \
        # - do we pass them into the main() function?
        cust_order = input("Is your order ready to go to the kitchen? Y/N:\n")
        if cust_order == ('Y').lower():
            print("Thanks. Sending your order to Vera in the kitchen...\n")
            orders_worksheet = SHEET.worksheet("Orders")
            orders_worksheet.append_row(cust_order)
            print("Your order has been received, please come and collect in 20 minutes.\n See you soon!\n")
        elif cust_order == ('N').lower():
            more_items = input("Would you like to order more pizzas? Y/N\n")
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
        return "Thanks Customer.name() for ordering a Size.size() Topping.topping()"


def main():
    """
    Run all main program functions
    """
    confirm_order()


print("Thank you for choosing Vera's Vegan Pizzas!\n")
print("Please follow the steps to place your order,")
print("then collect 20 minutes later.\n")
main()
"""
Libraries for supporting the application
"""
import re  # To validate mobile phone number
from datetime import datetime  # To add datetime to each order
import locale  # To set the currency for pizza prices
import gspread  # To open and edit pizza ordering spreadsheet
from google.oauth2.service_account import Credentials
from rich.console import Console  # Add styling to terminal to improve UX
from rich.traceback import install  # Render tracebacks with syntax formatting
from rich.table import Table


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vv_pizzas')
console = Console()
install(show_locals=True)
locale.setlocale(locale.LC_ALL, '')
currency = lambda x: locale.currency(x, grouping=True, symbol=True)


def get_customer_name():
    """
    Request and validate customers name
    """
    while True:
        name = console.input("Please provide your name:\n").lower()
        if name.isalpha():  # Validates the customer is characters only
            console.print(f"Hi {name.capitalize()} :waving_hand:\n")
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
            print(f"Thanks, we will use {telnum} to contact you if there are any issues.\n")
        else:
            print("Invalid number. 11 digits required, starting with 0, please try again\n")
            continue
        return telnum


def get_pizza():
    """
    Present the customer with the choice of pizza,
    and request a choice of 1-4
    """
    #  Table used to present menu to the customer
    pizza_table = Table()
    
    #  Data to populate the table of pizza choices
    pizza_table.add_column("Item", justify="center", vertical="middle")
    pizza_table.add_column("Pizza", justify="left", vertical="middle")
    pizza_table.add_column("Topping", justify="left", vertical="middle")

    pizza_table.add_row("1", "Margherita", "Vegan mozzarella and tomato")
    pizza_table.add_row("2", "Giardiniera", "Artichoke, mushrooms, red onion, black olives")
    pizza_table.add_row("3", "Diavolo", "Smoky jackfruits, green peppers, chilli oil")
    pizza_table.add_row("4", "Forza", "Chilli Quorn™, mixed peppers, sweet chilli peppers")

    print("Here are todays pizzas, which would you like?\n")
    console.print(pizza_table)

    # Request and validate the customers choice is between 1-4
    while True:
        pizza = int(
            input("Please choose a pizza by typing the item number, then click enter:\n"))
        if pizza == 1:
            console.print(":yum: a Margherita!\n")
            return 'Margherita'
        elif pizza == 2:
            console.print(":yum: a Giardiniera!\n")
            return 'Giardiniera'
        elif pizza == 3:
            console.print(":yum: a Diavolo!\n")
            return 'Diavolo'
        elif pizza == 4:
            console.print(":yum: a Forza!\n")
            return 'Forza'
        else:
            print("Invalid choice, please enter a number between 1-4\n")
            continue


def get_size():
    """
    Present the customer with the choice of sizes,
    and request a choice S, M, L
    """
    #  Table used to present sizes to the customer
    sizes_table = Table()

    #  Data to populate the table of pizza sizes
    sizes_table.add_column("Item", justify="center", vertical="middle")
    sizes_table.add_column("Name", justify="left", vertical="middle")
    sizes_table.add_column("Size", justify="left", vertical="middle")
    sizes_table.add_column("Price", justify="right", vertical="middle")

    sizes_table.add_row("S", "Small", "8 Inches", f"{currency(4.50)}")
    sizes_table.add_row("M", "Medium", "10 Inches", f"{currency(7.50)}")
    sizes_table.add_row("L", "Large", "14 Inches", f"{currency(4.50)}")

    print("Which size of pizza would you like?\n")
    console.print(sizes_table)

    #  Request and validate the customers choice is either S, M or L
    while True:
        size = input(
            "Please choose a size by entering the corresponding letter and clicking enter:\n"
            )
        if size.upper() == ('S'):
            print("Thanks, you chose Small\n")
            return 'Small'
        elif size.upper() == ('M'):
            print("Thanks, you chose Medium\n")
            return 'Medium'
        elif size.upper() == ('L'):
            print("Thanks, you chose Large\n")
            return 'Large'
        else:
            print("Invalid choice, please enter either S, M or L\n")
            continue


def get_price():
    """
    Receives input from get_size()
    to calculate the price for the order
    """


def get_time():
    """
    Provides ordering time
    Reformatted to be clearer
    Applied to each order within confirm_order()
    """
    time_now = datetime.now()
    order_time = time_now.strftime("%H:%M:%S")
    return order_time


def get_date():
    """
    Provides ordering date
    Reformatted to be clearer
    Applied to each order within confirm_order()
    """
    date_now = datetime.now()
    order_date = date_now.strftime("%d/%m/%Y")
    return order_date


def update_order_worksheet(data):
    """
    Send order to the Google Worksheet
    for the kitchen to process
    """
    print("Sending your order to Vera in the kitchen...\n")
    orders_worksheet = SHEET.worksheet("Orders")
    orders_worksheet.append_row(data)
    console.print(":thumbsup:")
    print("Your order has been received, please collect in 20 minutes\nSee you soon!\n")


def confirm_order():
    """
    Confirm the order back to the customer
    ask the customer to proceed Y/N
    provide an opportunity to order more items
    """
    name = get_customer_name()
    telnum = get_customer_number()
    pizza = get_pizza()
    size = get_size()
    order_time = get_time()
    order_date = get_date()
    #  Collate order data to be confirmed and sent to the kitchen
    cust_order = [
        name.capitalize(),
        telnum,
        pizza,
        size,
        order_time,
        order_date
        ]
    print(cust_order)
    #  Confirm order back to the customer CHANGE {} BELOW TO cust_ORDER
    console.print(f"Thanks {name.capitalize()}, you are ordering a {size} {pizza} :pizza:\n")

    while True:
        #  Request the customer to confirm if the order is complete
        #  If not complete, options to either add more items
        #  If not order more, amend existing order
        user_confirm = input(
            "Is your order ready to go to the kitchen? Y/N:\n"
            )
        if user_confirm == ('Y').lower():
            update_order_worksheet(cust_order)
        elif user_confirm == ('N').lower():
            more_items = input("Would you like to order more pizzas? Y/N\n")
            if more_items == ('Y').lower():
                print("I need to code how to add more items")
            elif more_items == ('N').lower():
                amend_order = input(
                    "Would you like to amend this order? Y/N\n"
                    )
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
    Including welcome message
    """
    console.print("[#008C45]Thank you[/] [#F4F5F0]for choosing[/] [#CD212A]Vera's Vegan Pizzas![/]\n", style="bold")
    print("Please follow the steps to place your order,")
    print("then collect 20 minutes later.\n")
    confirm_order()


main()

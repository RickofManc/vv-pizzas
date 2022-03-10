"""
Libraries for supporting the application
"""
import re  # To support name and phone number validation
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
        name = console.input("Please provide your name:\n").strip()
        if re.match(r"[\s\S\?]", name):  # Validates the customer is characters only
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
        num_pattern = re.compile(r"\d{11}")
        return num_pattern.match(telnum)
    # Requests telephone number, break if valid or provide error message
    while True:
        telnum = input("Please provide a mobile contact number:\n")
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
    menu = SHEET.worksheet("Pizzas").get_all_values()
    pizza_table = Table()
    
    pizza_table.add_column("Item", justify="center", vertical="middle")
    pizza_table.add_column("Pizza", justify="left", vertical="middle")
    pizza_table.add_column("Topping", justify="left", vertical="middle")

    pizza_table.add_row("1", "Margherita", "Vegan mozzarella and tomato")
    pizza_table.add_row("2", "Giardiniera", "Artichoke, mushrooms, red onion, black olives")
    pizza_table.add_row("3", "Diavolo", "Smoky jackfruits, green peppers, chilli oil")
    pizza_table.add_row("4", "Forza", "Chilli Quorn™, mixed peppers, sweet chilli peppers")

    #  Data to populate the table of pizza choices
    #  pizza_table.add_column("Item", justify="center", vertical="middle")
    #  pizza_table.add_column("Pizza", justify="left", vertical="middle")
    #  pizza_table.add_column("Topping", justify="left", vertical="middle")

    #  pizza_table.add_row("1", "Margherita", "Vegan mozzarella and tomato")
    #  pizza_table.add_row("2", "Giardiniera", "Artichoke, mushrooms, red onion, black olives")
    #  pizza_table.add_row("3", "Diavolo", "Smoky jackfruits, green peppers, chilli oil")
    #  pizza_table.add_row("4", "Forza", "Chilli Quorn™, mixed peppers, sweet chilli peppers")

    print("Here are todays pizzas, which would you like?\n")
    console.print(pizza_table)

    # Request and validate the customers choice is between 1-4
    while True:
        pizza = input("Please choose a pizza by typing the item number, then click enter:\n")
        if pizza == "1":
            console.print(":yum: a Margherita!\n")
            return 'Margherita'
        elif pizza == "2":
            console.print(":yum: a Giardiniera!\n")
            return 'Giardiniera'
        elif pizza == "3":
            console.print(":yum: a Diavolo!\n")
            return 'Diavolo'
        elif pizza == "4":
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
        cust_size = input(
            "Please choose a size by entering the corresponding letter and clicking enter:\n"
            )
        if cust_size.upper() == ("S"):
            cust_size = "Small"
            print("Thanks, you chose Small\n")
        elif cust_size.upper() == ("M"):
            cust_size = "Medium"
            print("Thanks, you chose Medium\n")
        elif cust_size.upper() == ("L"):
            cust_size = "Large"
            print("Thanks, you chose Large\n")
        else:
            print("Invalid choice, please enter either S, M or L\n")
            continue
        return cust_size


def get_quantity():
    """
    Asks the customer to specify 
    how many pizzas they would
    like to purchase
    """
    # Requests the customer inputs number of pizzas, break if valid or provide error message    
    while True:
        qty = int(input("How many would you like? (max 6 pizzas per person)\n"))
        if qty in range(1, 6, 1):
            return qty
        else:
            print("Invalid entry, please specify a number between 1-6\n")
            continue


def get_cost(cust_size, qty):
    """
    Receives input from get_size()
    to calculate the price for the order
    depending on the size request
    """
    cost = 0
    if cust_size == ("Small"):
        cost = qty * 4.50
    elif cust_size == ("Medium"):
        cost = qty * 7.50
    elif cust_size == ("Large"):
        cost = qty * 10.50
    return cost


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
    cust_size = get_size()
    qty = get_quantity()
    cost = get_cost(cust_size, qty)
    order_time = get_time()
    order_date = get_date()
    #  Collate order data to be confirmed and sent to the kitchen
    cust_order = [
        name.capitalize(),
        telnum,
        pizza,
        cust_size,
        qty,
        cost,
        order_time,
        order_date
        ]
    print(cust_order)
    #  Confirm order back to the customer CHANGE {} BELOW TO cust_ORDER
    console.print(f"Thanks {name.capitalize()}, please confirm your order is;\n {qty} {cust_size} {pizza} for {cost} :pizza:\n")

    while True:
        #  Request the customer to confirm if the order is complete
        #  If not complete, options to either add more items
        #  If not order more, amend existing order
        user_confirm = input(
            "Is your order ready to go to the kitchen? Y/N:\n"
            )
        if user_confirm.upper() == ('Y'):
            update_order_worksheet(cust_order)
        elif user_confirm.upper() == ('N'):
            more_items = input("Would you like to order more pizzas? Y/N\n")
            if more_items.upper() == ('Y'):
                print("I need to code how to add more items")
            elif more_items.upper() == ('N'):
                amend_order = input(
                    "Would you like to amend this order? Y/N\n"
                    )
                if amend_order.upper() == ('Y'):
                    print("I need to code how to amend the order")
                elif amend_order.upper() == ('N'):
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

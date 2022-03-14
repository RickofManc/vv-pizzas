"""
Imported libraries supporting the application
"""
import re  # To support name and phone number validation
from datetime import datetime  # To add datetime to each order
import time  # To add a pause between certain functions executing
import locale  # To set the currency for pizza prices
import gspread  # To open and edit pizza ordering spreadsheet
from google.oauth2.service_account import Credentials
from rich.console import Console  # Add styling to string for improved UX
from rich.traceback import install  # Render tracebacks with syntax formatting
from rich.table import Table  # To set the pizza and size options in a table
from rich.progress import track  # To add a progress bar for sending orders
from time import sleep  # To support the progress bar in sending orders


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vv_pizzas')
console = Console()  # Provides access to Rich console debugging
install(show_locals=True)  # Allows Rich display local variable values
locale.setlocale(locale.LC_ALL, '')  # Allows dynamic display local settings
# Code to adopt GBP £ symbol within pizza pricing table
GB_currency = lambda x: locale.currency(x, grouping=True, symbol=True)


def clear():
    """
    Clears the screen to allow for the next content to be displayed.
    Used primarily within place_order() to improve UX.
    """
    print('\033c')


def exit_to_main_menu():
    """
    Returns user to the Main Menu.
        Params:
            If 'E' returns user to Main Menu
            Else asks user to enter 'E'
        Returns:
            If valid navigates user to Main Menu
    """
    #  While loop to request and validate user enters 'E'
    while True:
        print("Enter E to exit to the main menu\n")
        exit_to_main = input("Enter your choice here:\n")
        if exit_to_main.upper() == ("E"):
            main()
        else:
            print("Invalid choice, please type E and click Enter")
            continue


def get_customer_name():
    """
    Requests and validates users name.
        Params:
            Requests user to input name and strip leading/lagging whitespaces
            If statement validates the input matches RE conditions
            Else requests the user tries again
        Returns:
            Print statement confirming input is valid
            Name (str): used within place_order()
    """
    #  While loop to request user inputs valid name
    #  If not valid, error message asks the user to try again
    while True:
        name = console.input("Please provide your name:\n").strip()
        if re.match(r"[\s\S\?]", name):
            console.print(f"Hi {name.capitalize()} :waving_hand:\n")
        else:
            print("Invalid name, please try again\n")
            continue
        return name


def get_customer_number():
    """
    Requests and validates users contact phone number.
        Params:
            While True user must enter 11 digit number starting with 0
            Validate_mobile() validate telnum variable using Re pattern match
            Else requests the user tries again
        Returns:
            Print statement confirming input is valid
            telnum (str): used within place_order()
    """
    def validate_mobile(telnum):
        """
        Validates user contact phone number.
            Params:
                telnum: input value from get_customer_number()
                Validates the number using RE Compile method
            Returns:
                telnum: to get_customer_number() while loop
        """
        num_pattern = re.compile(r"\d{11}")
        return num_pattern.match(telnum)
    #  While loop to request user inputs valid contact phone number
    #  If not valid, error message asks the user to try again
    while True:
        print("Please provide a mobile phone number, that starts with a zero"
              " and is 11 digits\n")
        telnum = input("Enter your number here:\n")
        if validate_mobile(telnum):
            print(f"Thanks, we will use {telnum} to contact you if"
                  " there are any issues.\n")
        else:
            print("Invalid number. 11 digits required, starting with 0,"
                  " please try again\n")
            continue
        return telnum


def get_pizza():
    """
    Provides a menu of todays pizzas, requesting user to choose from 1-4.
        Params:
            Receives data from external spreadsheet
            Populates table rows with this data
            While loop requests user to input a choice between 1-4
            Else requests the user tries again
        Returns:
            Print statement confirming input is valid
            {Pizza choice}(str): used within place_order()
    """
    #  Print statement to inform user of what content is displayed
    print("Here are todays menu, which pizza would you like?\n")
    #  Menu options for current days pizzas from external spreadsheet
    menu = SHEET.worksheet("Pizzas").get_all_values()
    #  Removes header row to allow for code based headers below
    menu.pop(0)
    #  Setting the table columns with headers for the external data to populate
    pizza_table = Table(show_header=True, header_style="bold")
    pizza_table.add_column("Item", justify="center", vertical="middle")
    pizza_table.add_column("Pizza", justify="left", vertical="middle")
    pizza_table.add_column("Topping", justify="left", vertical="middle")
    #  For loop to add the rows of data from 'menu'
    for row in zip(*menu):
        pizza_table.add_row(*row)

    #  Prints the table with todays pizza choices from data above
    console.print(pizza_table)

    #  While loop to request user inputs valid pizza choice between 1-4
    #  If not valid, error message asks the user to try again
    while True:
        print("Please select an option by entering a number between 1-4.\n")
        pizza = input("Enter your choice here:\n")
        if pizza == "1":
            console.print(":yum: a Margherita!\n")
            return "Margherita"
        elif pizza == "2":
            console.print(":yum: a Giardiniera!\n")
            return "Giardiniera"
        elif pizza == "3":
            console.print(":yum: a Diavolo!\n")
            return "Diavolo"
        elif pizza == "4":
            console.print(":yum: a Forza!\n")
            return "Forza"
        else:
            print("Invalid choice, please enter a number between 1-4\n")
            continue


def get_size():
    """
    Provides a table fo pizza sizes and prices,
    requesting user to input choice.
        Params:
            Receives data from external spreadsheet
            Populates table rows with this data
            While loop requests user to input either S, M or L
            Else requests the user tries again
        Returns:
            Print statement confirming input is valid
            cust_size: used within place_order()
    """
    #  Print statement to inform user of what content is displayed
    print("Which size of pizza would you like?\n")

    #  Table variable used to present sizes to the customer
    sizes_table = Table()

    #  Setting the table columns with headers for the external data to populate
    sizes_table.add_column("Item", justify="center", vertical="middle")
    sizes_table.add_column("Name", justify="left", vertical="middle")
    sizes_table.add_column("Size", justify="left", vertical="middle")
    sizes_table.add_column("Price", justify="right", vertical="middle")

    sizes_table.add_row("S", "Small", "8 Inches", f"{GB_currency(4.50)}")
    sizes_table.add_row("M", "Medium", "10 Inches", f"{GB_currency(7.50)}")
    sizes_table.add_row("L", "Large", "14 Inches", f"{GB_currency(10.50)}")

    #  Prints the table with todays pizza choices from data above
    console.print(sizes_table)

    #  While loop to request user inputs valid size of either S, M or L
    #  If not valid, error message asks the user to try again
    while True:
        print("Please select either S, M or L\n")
        cust_size = input("Enter your choice here:\n")
        if cust_size.upper() == ("S"):
            cust_size = "Small"
            print("Thanks, you chose Small\n")
            break
        elif cust_size.upper() == ("M"):
            cust_size = "Medium"
            print("Thanks, you chose Medium\n")
            break
        elif cust_size.upper() == ("L"):
            cust_size = "Large"
            print("Thanks, you chose Large\n")
            break
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
    # Requests the customer inputs number of pizzas,
    # break if valid or provide error message
    while True:
        print("How many would you like?")
        print("Please choose between 1-6\n")
        qty = int(input("Enter your choice here:\n"))
        if qty in range(1, 7, 1):
            break
        else:
            print("Invalid choice, please enter a number between 1-6\n")
            continue
    return qty


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
    return f"{GB_currency(cost)}"


def get_time():
    """
    Provides ordering time
    Reformatted to be clearer
    Applied to each order within place_order()
    """
    time_now = datetime.now()
    order_time = time_now.strftime("%H:%M:%S")
    return order_time


def get_date():
    """
    Provides ordering date
    Reformatted to be clearer
    Applied to each order within place_order()
    """
    date_now = datetime.now()
    order_date = date_now.strftime("%d/%m/%Y")
    return order_date


def update_order_worksheet(data):
    """
    Send order to the Google Worksheet
    for the kitchen to process
    """
    def send_order():
        sleep(0.015)
    
    for _ in track(range(100), description="[green]Sending order"
                                           " to the kitchen\n"):
        send_order()
    
    orders_worksheet = SHEET.worksheet("Orders")
    orders_worksheet.append_row(data)
    console.print(":thumbsup:\n")
    print("Your order has been received, please collect in 20 minutes\n")
    print("See you soon!\n")
    exit_to_main_menu()


def place_order():
    """
    Steps for the customer to place an order
    also provides an opportunity to order more items
    """
    clear()
    name = get_customer_name()
    telnum = get_customer_number()
    time.sleep(2.5)
    clear()
    pizza = get_pizza()
    time.sleep(2)
    clear()
    cust_size = get_size()
    qty = get_quantity()
    cost = get_cost(cust_size, qty)
    order_time = get_time()
    order_date = get_date()
    clear()

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
    console.print(f"Thanks {name.capitalize()}, you are ordering;\n"
                  f"{qty} {cust_size} {pizza} for {cost} :pizza:\n")

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
                    place_order()
                else:
                    print("Invalid choice, please enter either Y or N\n")
                    continue
            else:
                print("Invalid choice, please enter either Y or N\n")
                continue
        else:
            print("Invalid choice, please enter either Y or N\n")
            continue


def view_live_orders():
    """
    Get the data from the orders spreadsheet,
    remove the data from past days to leave
    todays orders to show the customer
    """
    print("Here comes the current live orders...\n")
    live_orders = SHEET.worksheet("Orders").get_all_values()
    live_orders.pop(0)  # remove headers to be added in view_live_orders 
    live_orders.insert(0, ["Name", "Phone Number", "Pizza", "Size", "Quantity", "Price", "Date", "Time"])
    print(live_orders)


def main():
    """
    Main menu screen complete
    with welcome message
    """
    while True:
        clear()
        console.print("[#008C45]Thank you[/] [#F4F5F0]for choosing[/]"
                      " [#CD212A]Vera's Vegan Pizzas![/]\n", style="bold")
        console.print("Main Menu", style="bold")
        print("1. Place An Order")
        print("2. View Live Orders")
        print("3. Exit Ordering System\n")
        print("Please select an option by entering a number between 1-3\n")

        selection = input("Enter your choice here:\n")

        if selection == "1":
            place_order()
        elif selection == "2":
            view_live_orders()
        elif selection == "3":
            print("Please come back soon - Bye Bye!")
            break
        else:
            print("Invalid choice, please enter a number between 1-3")
            continue


if __name__ == "__main__":
    # Execute main Python function
    main()

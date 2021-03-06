"""
Imported libraries supporting the application
"""
import re  # To support name and phone number validation
from datetime import datetime  # To add datetime to each order
import sys  # To provide the user with an exit from the ordering system
import time  # To add a pause between certain functions executing
from time import sleep  # To support the progress bar in sending orders
import random  # To create sequential order references
import pandas as pd  # To receive data from the external Google Sheet
from tabulate import tabulate  # To render pandas DataFrames
import gspread  # To open and edit pizza ordering spreadsheet
from google.oauth2.service_account import Credentials
from rich.console import Console  # Add styling to string for improved UX
from rich.traceback import install  # Render tracebacks with syntax formatting
from rich.progress import track  # To add a progress bar for sending orders


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vv_pizzas')
console = Console(highlight=False)  # Provides Rich formatting print()
install(show_locals=True)  # Allows Rich display local variable values


def clear():
    """
    Clears the screen to allow for the next content to be displayed.
    Used primarily within place_order() to improve UX.
    """
    print('\033c')


def get_customer_name():
    """
    Requests and validates users name.
    Provides opportunity for the user to exit to Main Menu.
        Params:
            Requests user to input name and strip leading/lagging whitespaces
            If statement validates the input matches RE conditions
            Else requests the user tries again
        Returns:
            Print statement confirming input is valid
            Name (str): used within place_order()
    """
    console.print("What would you like to do next?\n", style="bold")
    print("1. Continue to place your order")
    print("2. Exit to Main Menu\n")
    print("Please select an option by entering either 1 or 2\n")
    #  While loop to provide sub-menu options
    #  If not valid, error message asks the user to try again
    while True:
        selection = input("Enter your choice here:\n").strip()
        if selection == "1":
            break
        elif selection == "2":
            main()
        else:
            print("\nInvalid choice, please enter a number between 1-3\n")
            continue
    #  If option 1, While loop to request users details
    #  If not valid, error message asks the user to try again
    while True:
        clear()
        name = console.input("Please provide your name:\n").strip()
        if re.match(r"[\s\S\?]", name):
            console.print(f"Hi {name.title()} :waving_hand:\n")
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
    print("Please provide a mobile phone number, that starts with 07"
          " and is 11 digits\n")

    def validate_mobile(telnum):
        """
        Validates user contact phone number.
            Params:
                telnum: input value from get_customer_number()
                Validates the number using RE Compile method
            Returns:
                telnum: to get_customer_number() while loop
        """
        num_pattern = re.compile(r"^(07\d{9}|447\d{9})$")
        return num_pattern.match(telnum)
    #  While loop to request user inputs valid contact phone number
    #  If not valid, error message asks the user to try again
    while True:
        telnum = input("Enter your number here:\n")
        if validate_mobile(telnum):
            print(f"\nThanks, we will use {telnum} to contact you if"
                  " there are any issues.\n")
        else:
            print("\nInvalid number. 11 digits required, starting with 0,"
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
    console.print("Here's todays menu, which pizza would you like?"
                  "\n", style="bold")
    #  Menu options for current days pizzas from external spreadsheet
    menu_df = pd.DataFrame(SHEET.worksheet("Pizzas").get_all_records())
    print(tabulate(
        menu_df, headers='keys', tablefmt='pretty', showindex="never"))

    #  While loop to request user inputs valid pizza choice between 1-4
    #  Provides opportunity for the user to restart order or exit to Main Menu
    #  If not valid, error message asks the user to try again
    while True:
        console.print("\nPlease select an item and enter the number below\n"
                      "\nOr enter:\n"
                      "(R) to restart your order\n"
                      "(E) to exit to the Main Menu\n")
        pizza = input("Enter your choice here:\n").strip()
        if pizza == "1":
            console.print(":yum:\nMargherita!\n")
            return "Margherita"
        elif pizza == "2":
            console.print(":yum:\nGiardiniera!\n")
            return "Giardiniera"
        elif pizza == "3":
            console.print(":yum:\nDiavolo!\n")
            return "Diavolo"
        elif pizza == "4":
            console.print(":yum:\nForza!\n")
            return "Forza"
        elif pizza.upper() == "R":
            break
        elif pizza.upper() == "E":
            main()
        else:
            print("Invalid choice, please enter either a number between 1-4,"
                  "or letters R or E\n")
            continue
    place_order()


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
    console.print("Which size would you like?\n", style="bold")
    #  Options for pizza size and cost from external spreadsheet
    sizes_df = pd.DataFrame(SHEET.worksheet("Sizes").get_all_records())
    print(tabulate(
        sizes_df, headers='keys', tablefmt='pretty', showindex="never"))

    #  While loop to request user inputs valid size of either S, M or L
    #  Provides opportunity for the user to restart order or exit to Main Menu
    #  If not valid, error message asks the user to try again
    console.print("\nPlease select an item and enter the letter below\n"
                  "\nOr enter:\n"
                  "(R) to restart your order\n"
                  "(E) to exit to the Main Menu\n")
    while True:
        cust_size = input("Enter your choice here:\n").strip()
        if cust_size.upper() == "S":
            cust_size = "Small"
            print("Thanks, you chose Small\n")
            return cust_size
        elif cust_size.upper() == "M":
            cust_size = "Medium"
            print("Thanks, you chose Medium\n")
            return cust_size
        elif cust_size.upper() == "L":
            cust_size = "Large"
            print("Thanks, you chose Large")
            return cust_size
        elif cust_size.upper() == "R":
            break
        elif cust_size.upper() == "E":
            main()
        else:
            print("Invalid choice, please enter a size of either S, M or L\n"
                  "or R to Restart, E to Exit\n")
            continue
    place_order()


def get_quantity():
    """
    Provides a question to the user asking;
    How many pizzas they would like to order?
        Params:
            While loop requests user to input a choice between 1-6
            If valid while loop breaks
            Else requests the user tries again
        Returns:
            qty(int): used within place_order()
    """
    console.print("How many would you like?\n", style="bold")
    console.print("Please enter a quantity between 1-6 below\n"
                  "\nOr enter:\n"
                  "(R) to restart your order\n"
                  "(E) to exit to the Main Menu\n")
    #  While loop to request user inputs valid quantity between 1-6
    #  Provides opportunity for the user to restart order or exit to Main Menu
    #  If not valid, error message asks the user to try again
    while True:
        qty = input("Enter your choice here:\n").strip()
        if qty.isnumeric() == 1:
            return int(qty)
        if qty.isnumeric() == 2:
            return int(qty)
        if qty.isnumeric() == 3:
            return int(qty)
        if qty.isnumeric() == 4:
            return int(qty)
        if qty.isnumeric() == 5:
            return int(qty)
        if qty.isnumeric() == 6:
            return int(qty)
        elif qty.upper() == "R":
            break
        elif qty.upper() == "E":
            main()
        else:
            print("Invalid choice, please enter a number between 1-6\n"
                  "or R to Restart, E to Exit\n")
            continue
    place_order()


def get_cost(cust_size, qty):
    """
    Calculates the cost of the pizza
        Params:
            cust_size: users choice of size S, M or L
            qty: users choice of order quantity 1-6
            If statement used to multiply:
                cost of pizza size * quantity
        Returns:
            f string with calculated cost and GBP symbol
            Used within place_order()
    """
    pizza_cost = pd.DataFrame(SHEET.worksheet("Cost").get_all_records())
    if cust_size == ("Small"):
        cost = qty * pizza_cost.at[0, 'Cost']
    elif cust_size == ("Medium"):
        cost = qty * pizza_cost.at[1, 'Cost']
    elif cust_size == ("Large"):
        cost = qty * pizza_cost.at[2, 'Cost']
    return cost


def get_time():
    """
    Calculates the ordering time.
    Used in conjunction with get_date() within place_order().
    This helps inform the kitchen on the priority to execute orders.
        Params:
            uses time import module
            datetime.now method applied to time_now variable of current time
            format time_now into string literals using strftime method
        Returns:
            order_time: Used within place_order()
    """
    time_now = datetime.now()
    order_time = time_now.strftime("%H:%M")
    return order_time


def get_date():
    """
    Calculates the ordering date.
    Used in conjunction with get_time() within place_order().
    This helps inform the kitchen on the priority to execute orders.
        Params:
            uses time import module
            datetime.now method informs date_now variable of current date
            format date_now into string literals using strftime method
        Returns:
            order_date: Used within place_order()
    """
    date_now = datetime.now()
    order_date = date_now.strftime("%d/%m/%Y")
    return order_date


def get_reference():
    """
    Generates random number used as the order reference.
        Params:
            uses random module
            calculates 1 random number within a range of 1-2000
        Returns:
            order_ref: as a string value with square brackets removed
            Used within place_order()
    """
    order_ref = random.sample(range(1, 2000), 1)
    return str(order_ref).replace('[', '').replace(']', '')


def update_order_worksheet(data):
    """
    Inserts provided order data to external spreadsheet
    Encompasses functionality to illustrate a progress bar
    to the user whilst their order is being sent to the
    kitchen.
    """
    def send_order():
        """
        Using Sleep method from Time module and Rich Progress module
        a progress bar is displayed that takes 0.015 seconds
        to move from 0-100
            Params:
                Uses Track method from Progress module
                Sets a range of 0-100 and colour of Green
                For loop progress through the range,
                taking 0.015 seconds to complete
        """
        sleep(0.015)
    for _ in track(range(100), description="[green]Sending order to the"
                                           " kitchen\n"):
        send_order()
    #  Identifies the applicable worksheet from the external spreadsheet
    #  Appends the users order to the last row of that worksheet
    #  Print statement confirms the order has been sent to the kitchen
    #  Returns user back to the Main Menu after time to read the msg
    orders_worksheet = SHEET.worksheet("Orders")
    orders_worksheet.append_row(data)
    console.print(":thumbsup:\n")
    print("Your order has been received\n"
          "Please collect in 20 minutes using your reference\n")
    print("See you soon!\n")
    time.sleep(5)
    main()


def place_order():
    """
    Provides steps for the user to follow to order a pizza.
    Global functions are called in a logical order.
    These functions return values that are compiled into the order.
    While loop is used to ask the user to either;
        S. Send order to the kitchen
        R. Restart order
        E. Exit to main menu
    """
    #  Clears screen ready for next screen
    clear()
    #  Requests and returns the users name and contact phone number
    name = get_customer_name()
    telnum = get_customer_number()
    #  Sets a delay to allow time for user to read message
    time.sleep(2.5)
    #  Clears screen ready for next screen
    clear()
    # Receives return value
    pizza = get_pizza()
    #  Sets a delay to allow time for user to read message
    time.sleep(2)
    #  Clears screen ready for next screen
    clear()
    #  Requests and returns user choice of pizza size
    cust_size = get_size()
    #  Sets a delay to allow time for user to read message
    time.sleep(2)
    #  Clears screen ready for next screen
    clear()
    #  Requests and returns user required quantity
    qty = get_quantity()
    #  Calculates and returns the cost of the order
    cost = get_cost(cust_size, qty)
    #  Calculates and returns the ordering time and date
    order_time = get_time()
    order_date = get_date()
    #  Generates random order reference
    order_ref = get_reference()
    #  Clears screen ready for next screen
    clear()

    #  List collate the returned values from functions to confirm order
    cust_order = [
        order_ref,
        name.title(),
        telnum,
        pizza,
        cust_size,
        qty,
        cost,
        order_time,
        order_date
        ]

    #  Confirm order back to the customer and provide order reference
    console.print(f"Thanks {name.title()}, you are ordering;\n"
                  f"{qty} {cust_size} {pizza} for ??{cost:.2f} :pizza:\n"
                  f"Your reference for this order is {order_ref}\n")
    #  While loop to either send the confirmed order or restart
    #  If not a valid input, error message asks the user to try again
    console.print("\nIs your order ready to go to the kitchen?\n")
    console.print("\nPlease enter:\n"
                  "(S) to send your order\n"
                  "(R) to restart your order\n"
                  "(E) to exit to the Main Menu\n")
    while True:
        user_confirm = input("Enter your choice here:\n").strip()
        if user_confirm.upper() == "S":
            update_order_worksheet(cust_order)
        elif user_confirm.upper() == "R":
            break
        elif user_confirm.upper() == "E":
            main()
        else:
            print("Invalid choice, please enter a letter, either S, R or E\n")
            continue
    place_order()


def view_live_orders():
    """
    Displays the current live orders to the user so they can view
    the status of their order.
        Params:
            Uses Pandas DataFrame to display data from spreadsheet
            Removes columns with sensitive data; Phone Number, Cost
            Removes orders with 'Completed' status
        Returns:
            df: DataFrame with current live orders
    """
    clear()
    print("Here comes the current live orders...\n")
    orders_df = pd.DataFrame(SHEET.worksheet("Orders").get_all_records())
    orders_df = orders_df.drop(columns=["Phone Number", "Cost", "Date"])
    orders_df = orders_df[orders_df.Status != "Completed"]
    print(tabulate(
        orders_df, headers='keys', tablefmt='pretty', showindex="never"))

    #  While loop to request user inputs valid quantity between 1-3
    #  If not valid, error message asks the user to try again
    console.print("\nWhen ready, please choose from "
                  "the following options:\n", style="bold")
    print("1. Return to Main Menu")
    print("2. Place An Order")
    print("3. Exit Ordering System")
    while True:
        selection = input("\nEnter your choice here:\n").strip()
        if selection == "1":
            main()
        elif selection == "2":
            place_order()
        elif selection == "3":
            sys.exit("Please come back soon - Bye Bye!")
        else:
            print("Invalid choice, please enter a number between 1-3")
            continue


def main():
    """
    Execute first functionality for the user interface.
    Provides a welcome message and Main Menu with 3 choices.
        Params:
            Requests user to input a number between 1-3
            If statement executes a function dependent on input
            1: place_order()
            2: view_live_orders()
            3: exits system using sys.exit()
            Else requests the user tries again
    """
    clear()  # Clears any previous content to print welcome and menu below
    console.print("[#008C45]Thank you[/] [#F4F5F0]for choosing[/]"
                  " [#CD212A]Vera's Vegan Pizzas![/]\n", style="bold")
    console.print("Main Menu", style="bold")
    print("1. Place An Order")
    print("2. View Live Orders")
    print("3. Exit Ordering System\n")
    print("Please select an option by entering a number between 1-3\n")
    #  While loop to request user inputs valid quantity between 1-3
    #  If not valid, error message asks the user to try again
    while True:
        selection = input("Enter your choice here:\n").strip()
        if selection == "1":
            place_order()
        elif selection == "2":
            view_live_orders()
        elif selection == "3":
            sys.exit("Please come back soon - Bye Bye!")
        else:
            print("Invalid choice, please enter a number between 1-3")
            continue


if __name__ == "__main__":
    # Execute main Python function
    main()

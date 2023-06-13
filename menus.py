#!/usr/bin/python3
import time


class MenuDisplay:
    def __init__(self):
        # ANSI escape sequences for brighter colors
        self.colors = {
            'red': '\033[91;1m',
            'green': '\033[92;1m',
            'yellow': '\033[93;1m',
            'blue': '\033[94;1m',
            'purple': '\033[95;1m',
            'cyan': '\033[96;1m',
            'white': '\033[97;1m',
        }

        # Menu options with corresponding colors
        self.menu = [
            (self.colors['red'],"MySQL Menu MD Harrington London UK "),
            (self.colors['green'], "1. Check MySQL installation status"),
            (self.colors['yellow'], "2. Create 'Contacts' database"),
            (self.colors['blue'], "3. Create 'contact_names' table"),
            (self.colors['white'], "4. Add a new contact"),
            (self.colors['red'], "5. Find contact"),
            (self.colors['green'], "6. Find  and update contact"),
            (self.colors['yellow'], "7. Delete a contact "),
            (self.colors['purple'], "8. Exit"),

        ]
        

        # Search options with corresponding colors
        self.search_menu = [
            (self.colors['blue'],'Please enter criteria you ant to search on'),
            (self.colors['white'], '1. Name'),
            (self.colors['yellow'], '2. Surname'),
            (self.colors['red'], '3. Phone'),
            (self.colors['green'], '4. Email'),
            (self.colors['purple'], '5. Postcode'),
            (self.colors['white'], '6. Cancel'),
        ]

        

    def print_menu(self, options):
        # Print menu options in slow motion
        for i, (color, option) in enumerate(options):
            for char in option:
                print(color + char, end='', flush=True)
                time.sleep(0.025)  # Adjust the sleep duration for slower or faster printing
            print('\033[0m')  # Reset color after printing the option

            if i < len(options) - 1:
                print()  # Print a new line after each option, except for the last option

            time.sleep(0.1)  # Add a small delay before printing the next option

    def get_user_choice(self, options):
        while True:
            choice = input("Please enter your required selection: ")
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return int(choice)
            print("Invalid input. Please enter a valid menu option.")




#!/usr/bin/python3


''' Class menu  which will  display menus for various operations'''

import prompt_toolkit
import menus
import subprocess
import os
import getpass
import rsa 
import time 
from datetime import date
from datetime import datetime
import re
import string


class MySQLMngr:
    def __init__(self):
        self.installed = self.is_mysql_installed()
        self.username = None
        self.password = None
        os.system("clear")
  
    def generate_rsa_keys(self):
        publicKey, privateKey = rsa.newkeys(512)
        self.public_key = publicKey
        self.private_key = privateKey
       
    def encrypt(self, plaintext):
        ciphertext = rsa.encrypt(plaintext.encode(), self.public_key)
        return ciphertext.hex()

    def decrypt(self, ciphertext):
        plaintext = rsa.decrypt(bytes.fromhex(ciphertext), self.private_key)
        return plaintext.decode()
    
    def getDate(self):
        today = date.today()
        formatted_date = today.strftime("%y-%m-%d")
        return formatted_date
    
   
    def delay(self):
        time.sleep(1.5)

    
    def print_slow(self, text):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.028)  # Adjust the delay time as needed
        print()

    


    def is_mysql_installed(self):
        try:
            # Use the "mysql" command with the "--version" option to check if MySQL is installed
            subprocess.run(["mysql", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError:
            return False

    def print_status(self):
        if self.installed:
            self.print_slow("MySQL is installed.")
        else:
            self.print_slow("MySQL is not installed.")

   
    '''creates the database object if this doesent exist '''

    def create_database(self):
        
        if self.installed:
            

            command = f"mysql -u {self.username} -p{self.password} -e 'CREATE DATABASE IF NOT EXISTS Contacts;'"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)


            if "Contacts" in result.stdout:
                self.print_slow("Contacts database exists.")
            else:
                self.print_slow("Contacts database created successfully.")
        else:
            self.print_slow("MySQL is not installed. Unable to create the database. Please install mysql , mariadb first ")


    ''' creates table if doesnt exist '''

    def create_table(self):
        
        
        if self.installed:
            """  SQL Code 
            CREATE TABLE IF NOT EXISTS contact_names(
            ID VARCHAR(11) PRIMARY KEY, 
            date Date, 
            salutation VARCHAR(6),  
            name VARCHAR(25),
            surname VARCHAR(25), 
            email VARCHAR(40), 
            phone VARCHAR(25) , 
            postcode VARCHAR(20),
            UNIQUE KEY unique_id_name_surname (ID, Name, Surname)
            );
            """


            command = f"mysql -u {self.username} -p{self.password} Contacts -e \
            'CREATE TABLE IF NOT EXISTS contact_names \
            (ID VARCHAR(40) PRIMARY KEY, date Date, salutation VARCHAR(6),  name VARCHAR(25), \
            surname VARCHAR(25), email VARCHAR(40), phone VARCHAR(25) , postcode VARCHAR(20),\
            UNIQUE KEY unique_id_name_surname (ID, Name, Surname))'"

            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.print_slow("contact_names table created successfully. ")
            else:
                self.print_slow("Error creating the contact_names table. \n")
        else:
            self.print_slow("MySQL is not installed. Unable to create the table. \n")

    
    
    
    ''' This function  validates email'''    

    def is_valid_email(self , mail):
        # Regular expression pattern for email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, mail) is not None

    
    '''This function will iterate through list of strings  and  prompt  for input data into key value pair '''
    
    
    def getdetails(self):

        prompts = {
            "salutation": "Enter Salutation (e.g., Mr, Mrs): ",
            "name": "Enter contact name: ",
            "surname": "Enter contact surname: ",
            "email": "Enter contact email: ",
            "phone": "Enter contact phone: ",
            "postcode": "Enter contact postcode: "
        }

        details = {}
        for key, prompt in prompts.items():
            self.print_slow(prompt)
            details[key] = input().strip() # Remove leading/trailing whitespace

        return details


    def add_contact(self):
        if self.installed:

           

            while True:
                errorcounter = 0
                contact_details = self.getdetails()
                salutation = contact_details["salutation"]
                name = contact_details["name"]
                surname = contact_details["surname"]
                email = contact_details["email"]
                phone = contact_details["phone"]
                postcode = contact_details["postcode"]

                if not self.is_valid_email(email):
                    self.print_slow("Error: Invalid email address.")
                    errorcounter +=1 
                    continue

                # Validate the length of each field
                if len(salutation) > 6:
                    self.print_slow("Error: Salutation exceeds the maximum length.")
                    errorcounter +=1  
                    continue
                if len(name) > 25:
                    self.print_slow("Error: Name exceeds the maximum length.")
                    errorcounter +=1 
                    continue
                if len(surname) > 25:
                    self.print_slow("Error: Surname exceeds the maximum length.")
                    errorcounter +=1 
                    continue
                if len(email) > 40:
                    self.print_slow("Error: Email exceeds the maximum length.")
                    errorcounter +=1 
                    continue
                if len(phone) > 25:
                    self.print_slow("Error: Phone exceeds the maximum length.")
                    errorcounter +=1 
                    continue
                if len(postcode) > 20:
                    self.print_slow("Error: Postcode exceeds the maximum length.")
                    errorcounter +=1 
                    continue

                # No errors, proceed with the rest of the code
                date_str = self.getDate()  # Example date string
                date_obj = datetime.strptime(date_str, "%y-%m-%d").date()
                
                if errorcounter == 0 :
                    # concat to form ID

                    # remove white spaces  in postcode  f or use in ID

                    strpostCode = postcode.translate({ord(c): None for c in string.whitespace})

                    self.print_slow (f"PostCode is now for use id :{strpostCode}")
                    id               =     name[0]+surname[0]+phone[-6:]+ date_str + strpostCode
                    self.print_slow("ID is now: " + id)
                    input("Enter to continue")
                    # Add contact to the database
                    command = f"mysql -u {self.username} -p{self.password} Contacts -e \"USE Contacts; \
                    INSERT INTO contact_names (ID, salutation, date, name, surname, email, phone, postcode) \
                    VALUES ('{id}', '{salutation}', '{date_obj}', '{name}', '{surname}', '{email}', '{phone}', '{postcode}');\""

                    result = subprocess.run(command, shell=True, capture_output=True, text=True)

                    if result.returncode == 0:
                        self.print_slow("Contact added successfully.")
                        break  # Exit the loop on successful addition
                    else:
                        self.print_slow("Error adding the contact.")
        else:
            self.print_slow("MySQL is not installed. Unable to add the contact.")



    def set_credentials(self):
        self.username = input("Enter MySQL username: ")
        self.password = getpass.getpass("Enter MySQL password: ")

    def find_contact(self):

        if self.installed:
           

            search_term = input("Enter search term (name, surname, phone, or email): ")
            search_value = input("Enter search value: ")

            command = f"mysql -u {self.username} -p{self.password} Contacts -e  \"USE Contacts; SELECT * FROM contact_names WHERE {search_term} = '{search_value}';\""
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                search_results = result.stdout.strip().split("\n")
                if len(search_results) > 1:
                    self.print_slow("Search results:")
                    
                    
                for row in search_results[1:]:
                    self.print_slow(row)
                select = input("Please use enter key to go back to menu ")
                os.system("clear")

                
            else:
                self.print_slow("No matching contacts found.")
        else:
            self.print_slow("Error executing the search query.")

    def find_and_update_contact(self, search_term_number):
        if self.installed:
            search_term_map = {
                1: 'name',
                2: 'surname',
                3: 'email',
                4: 'phone',
                5: 'postcode'
            }
            
            self.print_slow("Enter search value: ")
            search_value = input()
            
            if search_term_number in search_term_map:
                search_term = search_term_map[search_term_number]
                
                command = f"mysql -u {self.username} -p{self.password} Contacts -e \"USE Contacts; SELECT * FROM contact_names WHERE {search_term} = '{search_value}';\""
                result = subprocess.run(command, shell=True, capture_output=True, text=True)

                if result.returncode == 0:
                    search_results = result.stdout.strip().split("\n")
                    if len(search_results) > 1:
                        self.print_slow("Search results:")
                        for row in search_results[1:]:
                            self.print_slow(row)

                        record_id = input("Enter the ID of the record to update: ")
                        field_name = input("Enter the name of the field to update (name, surname, email, phone, postcode): ")
                        new_value = input("Enter the new value: ")

                        update_command = f"mysql -u {self.username} -p{self.password} Contacts -e \"UPDATE contact_names \
                        SET {field_name} = '{new_value}' WHERE id = {record_id};\""


                        update_result = subprocess.run(update_command, shell=True, capture_output=True, text=True)

                        if update_result.returncode == 0:
                            self.print_slow("Record updated successfully.")
                        else:
                            self.print_slow("Error updating the record.")
                    else:
                        self.print_slow("No matching contacts found.")
                else:
                    self.print_slow("Error executing the search query.")
            else:
                self.print_slow("Invalid search term number. Please enter a valid number.")
        else:
            self.print_slow("MySQL is not installed. Unable to perform the search and update.")

        
        
   




def main():

    '''create instance of  MySQLChecker '''
    mysqlchecker = MySQLMngr()

    ''' create instance of menu '''
    menu = menus.MenuDisplay()


    ''' get user name and password for  mysql db , mariadb '''
    mysqlchecker.set_credentials()

    ''' generate  rsa keys for data encryption '''
    mysqlchecker.generate_rsa_keys()
  
    flag = True 
    

    while flag == True:
        
        
        mysqlchecker.delay()
        os.system("clear")

        menu.print_menu(menu.menu)
        user_choice = menu.get_user_choice(menu.menu)

        if user_choice == 1:

            mysqlchecker.print_slow("Option 1: Check MySQL installation status")

            mysqlchecker.print_status()

        elif user_choice == 2:

            mysqlchecker.print_slow("Option 2: Create 'Contacts' Database ")
            mysqlchecker.create_database()


        elif user_choice == 3:

            mysqlchecker.print_slow("Option 3: Create 'contact_names' table")
            mysqlchecker.create_table()

        elif user_choice == 4:

            mysqlchecker.print_slow("Option 4: Add a new contact")
            mysqlchecker.add_contact() 
            
        elif user_choice == 5:

            mysqlchecker.print_slow("Option 5: Find contact" )

        elif user_choice == 6:

            mysqlchecker.print_slow("Option 6: Find  and update contact")
            mysqlchecker.delay()
            os.system("clear")

            ''' show the menu for the  serach criteria'''
            menu.print_menu(menu.search_menu) 

            selcriteria = menu.get_user_choice(menu.search_menu)

            if selcriteria != 6:
                mysqlchecker.print_slow("Selected was : ", selcriteria)
                # pass this value to  find and update method 
                mysqlchecker.find_and_update_contact(selcriteria)
                
           


        elif user_choice == 7:

            mysqlchecker.print_slow("Option 7:  Delete a contact ")
            
        elif user_choice == 8:
            mysqlchecker.print_slow("Exiting... Thank you for using mysql , Maria DB")
            mysqlchecker.delay() 
            os.system("clear")
            flag = False
            exit()
    
   

''' call main '''          



if __name__ == '__main__':
    main()
''' Thanks for watching  I have more to do on this MD Harrington  Self Taught 
 Via  Utube usiing open  source  Who says it can be done  ?  
 I Just  have    Have a  good day
 
'''
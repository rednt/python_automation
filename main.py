
# Project roadmap
# Scope : - deleting emails older than {x} years
# Protocol : IMAP
# Goals : Delete emails based on conditions (e.g. older than {x} years , flagged as spam, etc)



import imaplib
import email
import nltk
import webbrowser
import os
import logging

from dotenv import load_dotenv
from email.header import decode_header
from nltk.metrics import edit_distance
from nltk.corpus import stopwords

# account credentials

load_dotenv('./env/.env') # Load the environment variables from the .env file [EMAIL, PASSWORD]

imap_server = "imap.gmail.com"
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def main():
    
    mail = connect_to_email()
    
    if mail:
        folder_list,cleaned_folder_list,full_folder_dict = list_folders(mail)
        search_condition(mail,folder_list,cleaned_folder_list)
        
        mail.logout()
        print("\nLogout successful.")

# Search for emails based on a condition

def search_condition(mail, folders,cleaned_folders):

    condition = input(
        "\nGive a condition to search for (examples: \n"
        "'FROM [folder name]', 'FROM UNSEEN', 'FROM BEFORE DD-MMM-YYYY',\n"
        "'UNSEEN', 'BEFORE DD-MMM-YYYY', 'SINCE DD-MMM-YYYY', etc.): "
    )
    print(f"\nProcessing condition: {condition}")
    
    # Check if the condition starts with "FROM"
    if condition.upper().startswith("FROM"):
        # Extract folder name or partial name
        parts = condition.split(maxsplit=1)
        if len(parts) < 2:
            print("Invalid condition. Please specify a folder or query after 'FROM'.")
            return
        folder_query = parts[1].split()[0]
        print(f"\033[0;32m{folder_query}\033[0m")
        
        
        # Find matching folders
        matching_folders = search_folder_nltk(folders,cleaned_folders, folder_query)
        if not matching_folders:
            print(f"No matching folders found for '{folder_query}'.")
            return
        elif len(matching_folders) > 1:
            print("\nMultiple matching folders found:")
            for i, folder in enumerate(matching_folders, 1):
                print(f"{i}. {folder}")
            try:
                choice = int(input("Enter the number of the folder to use: ")) - 1
                selected_folder = matching_folders[choice]
            except (ValueError, IndexError):
                print("Invalid selection.")
                return
        else:
            selected_folder = matching_folders[0]
        
        # Use the selected folder
        print(f"\nUsing folder: {selected_folder}")
        mail.select(selected_folder)
        
        # Remove "FROM [folder_query]" from the condition and process the rest
        remaining_condition = condition[len(f"FROM {folder_query}"):].strip()
    else:
        # If no "FROM", assume the default folder is selected (e.g., INBOX)
        mail.select("INBOX")
        remaining_condition = condition.strip()
    
    # Construct the search query
    try:
        if remaining_condition:
            status, email_ids = mail.search(None, f"{remaining_condition.upper()}")
        else:
            status, email_ids = mail.search(None, "ALL")  # Default to searching all emails

        # Handle the result
        if status == "OK" and email_ids[0] != b'':
            email_list = email_ids[0].split()
            print(f"Found {len(email_list)} emails matching the condition '{condition}'.")
        else:
            print(f"No emails found for the condition '{condition}'.")
    except imaplib.IMAP4.error as e:
        print(f"An error occurred while searching for emails: {e}")

def search_folder_nltk(folders,cleaned_folders,query):
    threshold = 2  # Adjust for stricter or looser matching
    matches = [folder for folder, cleaned_folder in zip(folders, cleaned_folders) 
               if edit_distance(cleaned_folder.lower(), query.lower()) <= threshold]
    return matches

def list_folders(mail):
    status, folders = mail.list()
    folder_list = []
    cleaned_folder_list = []  # List to store cleaned folder names for easier matching
    full_folder_dict = {}  # Dictionary to map cleaned folder names to full folder names

    if status == "OK":
        print("Available folders:\n")
        for folder in folders:
            # Decode the folder name
            parts = folder.decode().split(' "/" ')
            full_folder_name = parts[1].strip('"')
            
            # Clean the folder name (remove [Gmail] prefix)
            cleaned_folder_name = full_folder_name
            if full_folder_name.startswith("[Gmail]"):
                cleaned_folder_name = full_folder_name.replace("[Gmail]/", "").strip()

            # Add to the lists
            folder_list.append(full_folder_name)  # Original folder name for usage
            cleaned_folder_list.append(cleaned_folder_name)  # Cleaned folder name for matching
            full_folder_dict[cleaned_folder_name] = full_folder_name  # Map cleaned to full name
            
            print(f"- {cleaned_folder_name}")  # Show the cleaned folder name for matching
            
    else:
        print("Could not retrieve folder list.")
    
    return folder_list, cleaned_folder_list, full_folder_dict        

# Connect to the email server
def connect_to_email():
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        # Login to the account
        mail.login(username, password)
        print("\nLogin successful.\n")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"\nFailed to login: {e}")
        return None

if __name__ == "__main__":
    main()





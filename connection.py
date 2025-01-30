import imaplib
import os
from dotenv import load_dotenv
# account credentials

load_dotenv('./env/.env') # Load the environment variables from the .env file [EMAIL, PASSWORD]

imap_server = "imap.gmail.com"
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

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


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
from nltk import word_tokenize
from nltk.corpus import stopwords

# account credentials

load_dotenv('./env/.env') # Load the environment variables from the .env file [EMAIL, PASSWORD]

imap_server = "imap.gmail.com"
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def main():
    mail = connect_to_email()
    print("Login successful.")
    if mail:
        mail.select("inbox")
        search_condition(mail)
        
        mail.logout()
        print("Logout successful.")

# Search for emails based on a condition

def search_condition(mail):
    condition = input("Give me a condition to search for (options: UNSEEN, BEFORE DD-MMM-YYYY, SINCE DD-MMM-YYYY): ")
    print(f"Searching for emails with condition: {condition}")
    if condition.upper() == "UNSEEN":
        status, email_ids = mail.search(None, "UNSEEN")
    elif condition.upper().startswith("BEFORE"):
        try:
            date = condition.split(" ")[1]
            status, email_ids = mail.search(None, f'BEFORE "{date}"')
            print(f"Number of emails found: {len(email_ids[0].split())}")
        except IndexError:
            print("Invalid date format. Please use 'BEFORE DD-MMM-YYYY'.")
            return
    elif condition.upper().startswith("SINCE"):
        try:
            date = condition.split(" ")[1]
            status, email_ids = mail.search(None, f'SINCE "{date}"')
            print(f"Number of emails found: {len(email_ids[0].split())}")
        except IndexError:
            print("Invalid date format. Please use 'SINCE DD-MMM-YYYY'.")
            return
    else:
        print("Invalid condition. Please use 'UNSEEN' or 'BEFORE DD-MMM-YYYY' or 'SINCE DD-MMM-YYYY'.")
        return

    email_list = email_ids[0].split()
    print(f"Found {len(email_list)} emails matching the condition '{condition}'.")


def fetch_email(mail, email_list):
    for msg_id in email_list:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        

# Connect to the email server
def connect_to_email():
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        # Login to the account
        mail.login(username, password)
        print("Login successful!")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"Failed to login: {e}")
        return None




if __name__ == "__main__":
    main()





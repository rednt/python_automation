import imaplib
import logging
import os
from dotenv import load_dotenv
# account credentials

load_dotenv('./env/.env') # Load the environment variables from the .env file [EMAIL, PASSWORD]

imap_server = "imap.gmail.com"
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)
    
# Connect to the email server
def connect_to_email():
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        # Login to the account
        mail.login(username, password)
        logging.info('Login successful')
        print("\nLogin successful.\n")
        return mail
    except imaplib.IMAP4.error as e:
        logging.error(f"\nFailed to login: {e}")
        print(f"\nFailed to login: {e}")
        return None

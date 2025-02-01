import imaplib
import logging
from declutter_rules import filterIds
logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)

def search_condition(mail, condition):  
    try:
        status, email_ids = mail.search(None, condition.strip().upper()) 
        print(f"DEBUG: Searching with condition: '{condition.strip().upper()}'")
        # Handle the result and exclude Important and Updates folders
        if status == "OK" and email_ids[0] != b'':
            
            email_ids = email_ids[0].split()
           
            filtered_email_list = filterIds(mail,email_ids)
            
            print(f"Found {len(filtered_email_list)} emails matching the condition {f"{condition}"} .")
            logging.info(f"Found {len(filtered_email_list)} emails matching the condition {f"{condition}"} .")
            return filtered_email_list
        else:
            print(f"No emails found for the condition '{condition}'.")
            logging.info(f"No emails found for the condition '{condition}'.")
            return []
    except imaplib.IMAP4.error as e:
        print(f"An error occurred while searching for emails: {e}")
        logging.error(f"An error occurred while searching for emails: {e}")
        return []




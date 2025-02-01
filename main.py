
# Project roadmap
# Scope : - deleting emails older than {x} years
# Protocol : IMAP
# Goals : Delete emails based on conditions (e.g. older than {x} years , flagged as spam, etc)

import logging
from nltk.corpus import stopwords
from search import search_condition
from connection import connect_to_email
from declutter_rules import move_to_trash, archive_emails

logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)

def main():
    
    mail = connect_to_email()
    mail.select('"[Gmail]/All Mail"')
    if mail:
        
        condition = input(
        "\nGive a condition to search for (Excludes Important and Updates folders)\n"
        "('UNSEEN', 'BEFORE DD-MMM-YYYY', 'SINCE DD-MMM-YYYY', 'SEEN', 'UNSEEN BEFORE', 'UNSEEN SINCE', 'SEEN BEFORE' 'SEEN SINCE'): "
        )
        print(f"\nProcessing condition: {condition}")

        email_ids = search_condition(mail, condition)
        quit = 0
        while quit == 0:
            print("\nChoose an action to perform:\n")
            print("1. Move emails to Trash")
            print("2. Archive emails")
            print("3. Quit")
            action = input("\nEnter the action number: ")
            if action == "1":
                move_to_trash(mail, email_ids)
            elif action == "2":
                archive_emails(mail, email_ids)
            elif action == "3":
                quit = 1
            else:
                print("Invalid action number. Please try again.")
        
        

        mail.logout()
        logging.info('Logout successful')
        print("\nLogout successful.")



if __name__ == "__main__":
    main()







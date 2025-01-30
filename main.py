
# Project roadmap
# Scope : - deleting emails older than {x} years
# Protocol : IMAP
# Goals : Delete emails based on conditions (e.g. older than {x} years , flagged as spam, etc)

import logging
from nltk.corpus import stopwords
from search import search_condition
from connection import list_folders, connect_to_email
from declutter_rules import move_to_trash, archive_emails

logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)

def main():
    
    mail = connect_to_email()
    
    if mail:
        folder_list,cleaned_folder_list = list_folders(mail)
        email_ids = search_condition(mail,folder_list,cleaned_folder_list)
        
        
        

        mail.logout()
        logging.info('Logout successful')
        print("\nLogout successful.")



if __name__ == "__main__":
    main()







import imaplib 
import logging


logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)

def move_to_trash(mail, email_ids):
    try:
        trash_folder = "[Gmail]/Trash"  # Gmail trash folder 
        
        # Move the emails to the trash folder
        for email_id in email_ids:
            status, _ = mail.copy(email_id, trash_folder)
            if status != "OK":
                raise imaplib.IMAP4.error(f"Failed to copy email ID {email_id} to Trash.")
            
        # Mark emails as deleted in the current folder
        for email_id in email_ids:
            mail.store(email_id, "+FLAGS", "\\Deleted")
        logging.info(f"Marked {len(email_ids)} emails for deletion.")    
        # Expunge the mailbox to permanently delete marked emails
        mail.expunge()
        print(f"Moved {len(email_ids)} emails to the Trash.")
        logging.info(f"Moved {len(email_ids)} emails to the Trash.")
    
    except imaplib.IMAP4.error as e:
        logging.error(f"Error moving emails to Trash: {e}")
        print(f"An error occurred while moving emails to the Trash: {e}")


def archive_emails(mail, email_list):
    archive_folder = "Archive"
    try:
        mail.create(archive_folder)
    except:
        pass  # Ignore if the folder already exists

    for msg_id in email_list:
        mail.copy(msg_id, archive_folder)
        mail.store(msg_id, "+FLAGS", "\\Deleted")

    mail.expunge()
    print(f"Archived {len(email_list)} emails to the '{archive_folder}' folder.")
    logging.info(f"Archived {len(email_list)} emails to the '{archive_folder}' folder.")

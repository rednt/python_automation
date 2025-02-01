import imaplib 
import logging

logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)

def move_to_trash(mail, email_ids):
    try:
        email_ids = filterIds(mail, email_ids)
        trash_folder = "[Gmail]/Trash"  # Gmail trash folder 

        if not email_ids:
            print("No emails to move (all were in Updates or Important).")
            return
        
        # Move the emails to the trash folder
        for email_id in email_ids:
            status, _ = mail.copy(email_id, trash_folder)
            
            print(f"Moving email ID {email_id} to Trash.")
            if status != "OK":
                raise imaplib.IMAP4.error(f"Failed to copy email ID {email_id} to Trash.")
            
        # Mark emails as deleted in the current folder
        for email_id in email_ids:
            mail.store(email_id, "+FLAGS", "\\Deleted")
            print(f"Marked email ID {email_id} for deletion.")
        logging.info(f"Marked {len(email_ids)} emails for deletion.") 

        # Expunge the mailbox to permanently delete marked emails
        mail.expunge()
        print(f"Moved {len(email_ids)} emails to the Trash.")
        logging.info(f"Moved {len(email_ids)} emails to the Trash.")
    
    except imaplib.IMAP4.error as e:
        logging.error(f"Error moving emails to Trash: {e}")
        print(f"An error occurred while moving emails to the Trash: {e}")


def archive_emails(mail, email_ids):
    archive_folder = "Archive"
    email_ids = filterIds(mail, email_ids)
    try:
        mail.create(archive_folder)
    except:
        pass  # Ignore if the folder already exists
    try:
        if not email_ids:
            print("No emails to archive (all were in Updates or Important).")
            return
        for msg_id in email_ids:
            mail.copy(msg_id, archive_folder)
            mail.store(msg_id, "+FLAGS", "\\Deleted")
            print(f"Archiving email ID {msg_id}.")
    
    except imaplib.IMAP4.error as e:
        print(f"Error archiving emails: {e}")

    mail.expunge()
    print(f"Archived {len(email_ids)} emails to the '{archive_folder}' folder. (excluding Updates & Important).")
    logging.info(f"Archived {len(email_ids)} emails to the '{archive_folder}' folder. (excluding Updates & Important).")

def filterIds(mail,email_ids):
    return [email_id for email_id in email_ids if not is_email_excluded(mail, email_id)]

def is_email_excluded(mail, email_id):
    status, data = mail.fetch(email_id, "(X-GM-LABELS)")
    if status == "OK":
        labels = data[0].decode() if isinstance(data[0], bytes) else ""
        if "\\important" in labels.lower() or "category_updates" in labels.lower():
            return True
    return False
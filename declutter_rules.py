import imaplib 
import logging

logging.basicConfig(filename='email_cleaner.log', level=logging.DEBUG)

def move_to_trash(mail, email_ids):
    try:
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

def filterIds(mail, email_ids):
    filtered_emails = []
    seen_email_ids = set()
    i = 0
    for email_id in email_ids:
        if email_id in seen_email_ids:
            continue
        seen_email_ids.add(email_id)
        try:
            if not is_email_excluded(mail, email_id):
                i+=1
                filtered_emails.append(email_id)
        except Exception as e:
            print(f"Error processing email {email_id}: {e}")
            logging.error(f"Error processing email {email_id}: {e}")
    print(len(filtered_emails), " emails processed")
    print(len(email_ids)-len(filtered_emails), " emails excluded")
    logging.info(f"{len(filtered_emails)} emails processed")
    logging.info(f"{len(email_ids)-len(filtered_emails)} emails excluded")
    return filtered_emails




def is_email_excluded(mail, email_id):
    try:
        result, data = mail.fetch(email_id, "(X-GM-LABELS)")
        if result != "OK" or not data:
            print(f"Error fetching labels for email {email_id}: {data}")
            return False

        # Combine all returned parts into a single string.
        # The comprehension handles both bytes and tuple elements.
        all_labels = " ".join(
            part.decode("utf-8", errors="ignore") 
            if isinstance(part, bytes) 
            else part[1].decode("utf-8", errors="ignore") 
            for part in data if part
        )
        print(f"DEBUG: Combined label data for email {email_id}: {all_labels}")

        # Now check if the combined string contains the target labels.
        if '\\Important' in all_labels or '\\Updates' in all_labels:
            print(f"Excluding email {email_id} due to label match.")
            
            return True

        return False

    except Exception as e:
        print(f"Error checking email {email_id}: {e}")
        return False

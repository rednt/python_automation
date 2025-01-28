import imaplib
import email
import nltk
import webbrowser
import os

from dotenv import load_dotenv
from email.header import decode_header
from nltk import word_tokenize
from nltk.corpus import stopwords

# account credentials

load_dotenv('./env/.env')

imap_server = "imap.gmail.com"
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


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
    mail = connect_to_email()
    if mail:
        
        
        mail.logout()
        print("Logout successful!")



"""for email_id in email_ids[-1:]:
    status, msg_data = mail.fetch(email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Parse the message into an email object
            msg = email.message_from_bytes(response_part[1])

            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # If it's a bytes type, decode to str
                subject = subject.decode(encoding if encoding else "utf-8")
            print("Subject:", subject)

            # Decode the sender's email address
            from_ = msg.get("From")
            print("From:", from_)

            # If the email message is multipart
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" not in content_disposition:
                        # Get the email body
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True)
                            print("Body:", body.decode())
            else:
                # The email body is not multipart
                body = msg.get_payload(decode=True)
                print("Body:", body.decode())

# Logout from the server
mail.logout()"""



import imaplib
from nltk.metrics.distance import edit_distance
def search_condition(mail, folders,cleaned_folders):

    condition = input(
        "\nGive a condition to search for (examples: \n"
        "'FROM [folder name]', 'FROM UNSEEN', 'FROM BEFORE DD-MMM-YYYY',\n"
        "'UNSEEN', 'BEFORE DD-MMM-YYYY', 'SINCE DD-MMM-YYYY', etc.): "
    )
    print(f"\nProcessing condition: {condition}")
    
    # Check if the condition starts with "FROM"
    if condition.upper().startswith("FROM"):
        # Extract folder name or partial name
        parts = condition.split(maxsplit=1)
        if len(parts) < 2:
            print("Invalid condition. Please specify a folder or query after 'FROM'.")
            return
        folder_query = parts[1].split()[0]
        print(f"\033[0;32m{folder_query}\033[0m")
        
        
        # Find matching folders
        matching_folders = search_folder_nltk(folders,cleaned_folders, folder_query)
        if not matching_folders:
            print(f"No matching folders found for '{folder_query}'.")
            return
        elif len(matching_folders) > 1:
            print("\nMultiple matching folders found:")
            for i, folder in enumerate(matching_folders, 1):
                print(f"{i}. {folder}")
            try:
                choice = int(input("Enter the number of the folder to use: ")) - 1
                selected_folder = matching_folders[choice]
            except (ValueError, IndexError):
                print("Invalid selection.")
                return
        else:
            selected_folder = matching_folders[0]
        
        # Use the selected folder
        print(f"\nUsing folder: {selected_folder}")
        mail.select(selected_folder)
        
        # Remove "FROM [folder_query]" from the condition and process the rest
        remaining_condition = condition[len(f"FROM {folder_query}"):].strip()
    else:
        # If no "FROM", assume the default folder is selected (e.g., INBOX)
        mail.select("INBOX")
        remaining_condition = condition.strip()
    
    # Construct the search query
    try:
        if remaining_condition:
            status, email_ids = mail.search(None, f"{remaining_condition.upper()}")
        else:
            status, email_ids = mail.search(None, "ALL")  # Default to searching all emails

        # Handle the result
        if status == "OK" and email_ids[0] != b'':
            email_list = email_ids[0].split()
            print(f"Found {len(email_list)} emails matching the condition '{condition}'.")
        else:
            print(f"No emails found for the condition '{condition}'.")
    except imaplib.IMAP4.error as e:
        print(f"An error occurred while searching for emails: {e}")

def search_folder_nltk(folders,cleaned_folders,query):
    threshold = 2  # Adjust for stricter or looser matching
    matches = [folder for folder, cleaned_folder in zip(folders, cleaned_folders) 
               if edit_distance(cleaned_folder.lower(), query.lower()) <= threshold]
    return matches
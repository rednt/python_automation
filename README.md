# Python automation
## Email de-clutter
A Python script to declutter your Gmail inbox by automatically organizing emails based on custom search conditions.

### Features
- Search emails using various conditions (UNSEEN, SEEN, BEFORE date, SINCE date)
- Exclude Important and Updates folders from operations
- Move emails to Trash
- Archive emails
- Logging of operations

### Prerequisites
- Python 3.12
- Gmail account with IMAP enabled
- `.env` file with EMAIL and PASSWORD credentials

### Usage
1. Set up environment variables in `.env` file
2. Run the script
3. Enter search conditions when prompted
4. Choose from available actions:
    - Move to Trash
    - Archive emails
    - Change search condition
    - Quit

### Search Conditions
- `UNSEEN`: Unread emails
- `SEEN`: Read emails
- `BEFORE DD-MMM-YYYY`: Emails before date
- `SINCE DD-MMM-YYYY`: Emails after date
- Combinations like `UNSEEN BEFORE` or `SEEN SINCE`

### ⚠️ Warning
- Use at your own risk - script provided as-is
- Test with small email batch first
- Backup important emails before use

### Contributions
Contributions to improve this script are welcome! Feel free to:
- Submit pull requests
- Improve documentation

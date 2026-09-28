import importlib

# importing from 1_email_utils.py to keep this file short and readable
email_utils = importlib.import_module("1_email_utils")


def read_emails(count=5):
    return email_utils.fetch_emails(count)


def send_email(to, subject, body):
    print(f"\nTo: {to}\nSubject: {subject}\n\n{body}\n")
    if input("Send this email? (y/n): ").lower() != "y":
        return "User cancelled sending"
    return email_utils.send_email(to, subject, body)


functions = {"read_emails": read_emails, "send_email": send_email}

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_emails",
            "description": "Read the latest emails from the user's Gmail inbox, newest first.",
            "parameters": {
                "type": "object",
                "properties": {"count": {"type": "integer", "description": "How many emails to read (default 5)"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email from the user's Gmail account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    }
]

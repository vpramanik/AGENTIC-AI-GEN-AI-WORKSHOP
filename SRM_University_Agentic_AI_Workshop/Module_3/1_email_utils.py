import os
import email
import imaplib
import smtplib
from email.header import decode_header, make_header
from email.message import EmailMessage


def get_credentials():
    return os.environ["GMAIL_ADDRESS"], os.environ["GMAIL_APP_PASSWORD"]


def decode(value):
    return str(make_header(decode_header(value or "")))


def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            is_attachment = "attachment" in str(part.get("Content-Disposition"))
            if part.get_content_type() == "text/plain" and not is_attachment:
                return part.get_payload(decode=True).decode(errors="ignore")
        return ""
    return msg.get_payload(decode=True).decode(errors="ignore")


def fetch_emails(count=5):
    address, password = get_credentials()

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(address, password)
    mail.select("INBOX", readonly=True)

    _, data = mail.search(None, "ALL")
    email_ids = data[0].split()[-count:][::-1]

    emails = []
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        emails.append({
            "from": decode(msg["From"]),
            "subject": decode(msg["Subject"]),
            "date": msg["Date"],
            "body": get_body(msg).strip()[:500],
        })

    mail.logout()
    return emails


def send_email(to, subject, body):
    address, password = get_credentials()

    msg = EmailMessage()
    msg["From"] = address
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(address, password)
        server.send_message(msg)

    return f"Email sent to {to}"

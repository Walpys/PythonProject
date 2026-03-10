import smtplib
import asyncio
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def sync_send(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)
    return True

async def send_email(to_email, subject="Job Application", body="..."):
    try:
        result = await asyncio.to_thread(sync_send, to_email, subject, body)
        print(f"--- SUCCESS: Email sent to {to_email} ---")
        return result
    except Exception as e:
        print(f"Email Error: {e}")
        return False

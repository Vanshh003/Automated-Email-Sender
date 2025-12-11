import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import time

# Your Gmail credentials
SENDER_EMAIL = "vansh.agg003@gmail.com"
APP_PASSWORD = "egbgxsbkxjsytcuv"

# Subject of your email
SUBJECT = "Regarding Software Engineer Job Opportunities"

# Email body template
BODY_TEMPLATE = """
"""


# Attach your resume (optional)
ATTACHMENT_PATH = "Vansh_Resume.pdf"  # keep it in same directory

def send_email(name, company, receiver_email):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = SUBJECT

    # Format email body
    body = BODY_TEMPLATE.format(name=name, company=company)
    msg.attach(MIMEText(body, "plain"))

    # Attach resume
    try:
        with open(ATTACHMENT_PATH, "rb") as f:
            from email.mime.base import MIMEBase
            from email import encoders
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={ATTACHMENT_PATH}")
            msg.attach(part)
    except FileNotFoundError:
        print("Resume not found, skipping attachment.")

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print(f"✅ Email sent to {name} ({receiver_email}) at {company}")

# Read CSV and send emails
with open("recruiters-2.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        send_email(row["name"], row["company"], row["receiver_email"])
        time.sleep(30)  # wait 30 sec between emails to avoid Gmail limits

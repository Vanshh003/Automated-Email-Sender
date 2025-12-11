# Gmail Recruiter Outreach Script

A small Python script that reads a CSV of recruiter contacts and sends a tailored outreach email (optionally with your resume attached) using Gmail's SMTP server.

> **Warning / Ethics:** Use this responsibly. Only email people whose contact info is public and for whom outreach is appropriate. Follow anti-spam laws and the recipient platform's terms of service.

---

## Features

* Reads recruiter contacts from a CSV file
* Sends a personalized email to each contact
* Optionally attaches a resume PDF
* Built-in delay between sends to reduce chance of hitting Gmail limits

---

## Prerequisites

* Python 3.7+
* A Gmail account with an **App Password** (recommended) or appropriate SMTP access
* `recruiters-2.csv` file in the same directory as the script
* (Optional) `Vansh_Resume.pdf` in the same directory if you want to attach your resume

---

## Install

No external libraries are required; the script uses Python's standard library. Still, create a virtual environment if you prefer:

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate     # Windows
```

---

## Configuration

Open the script and update the top constants:

```python
SENDER_EMAIL = "your.email@gmail.com"
APP_PASSWORD = "your_app_password"
SUBJECT = "Regarding Software Engineer Job Opportunities"
BODY_TEMPLATE = """
Hi {name},\n\nI hope you are doing well. I came across your profile and wanted to reach out regarding opportunities at {company}. I recently graduated / interned at ... (customize).\n\nBest,\nYour Name\n"""
ATTACHMENT_PATH = "Vansh_Resume.pdf"
```

**Security tip:** Do NOT hardcode credentials into the file if you plan to store the repo anywhere. Instead use environment variables (example below) or a `.env` file that is in `.gitignore`.

Example using environment variables (recommended):

```python
import os
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
APP_PASSWORD = os.environ.get('APP_PASSWORD')
```

Set variables on macOS / Linux:

```bash
export SENDER_EMAIL="your.email@gmail.com"
export APP_PASSWORD="your_app_password"
```

On Windows (PowerShell):

```powershell
$env:SENDER_EMAIL = "your.email@gmail.com"
$env:APP_PASSWORD = "your_app_password"
```

---

## Gmail App Password

If you have 2-Step Verification enabled (recommended), create an App Password for "Mail" and use it in `APP_PASSWORD`. Do not use your normal account password. If you do not use 2FA, Google may block sign-in from less-secure apps — using an App Password with 2FA is the safer approach.

---

## CSV Format

The script expects a CSV named `recruiters-2.csv` with a header and these columns (case-sensitive):

```csv
name,company,receiver_email
John Doe,Acme Corp,john.doe@example.com
Jane Smith,Example Inc,jane.smith@example.com
```

Adjust the header names in code if your CSV uses different column names.

---

## Usage

1. Ensure the CSV and (optionally) `Vansh_Resume.pdf` are in the same directory as the script.
2. Configure credentials and `BODY_TEMPLATE`.
3. Run the script:

```bash
python send_recruiter_emails.py
```

The script prints a confirmation for each sent email and sleeps 30 seconds between sends by default (modify `time.sleep(30)` if you want a different delay).

---

## Rate Limits & Best Practices

* Gmail imposes sending limits (per day and per minute). Typical free accounts have low daily limits. Abide by those limits to avoid being temporarily blocked.
* Keep delays between messages (30s is a conservative starting point). If you plan to send many messages, consider using a professional email service (Mailgun, SendGrid, AWS SES) that supports bulk sending.
* Personalize each message (the template supports `{name}` and `{company}`) to improve response rate.

---

## Troubleshooting

* `smtplib.SMTPAuthenticationError`: Check credentials and whether App Password is needed.
* `smtplib.SMTPRecipientsRefused`: Verify the email addresses in the CSV.
* Attachment not found: Make sure `Vansh_Resume.pdf` exists or remove/adjust the attachment code.

---

## Customization Ideas

* Use HTML email bodies (`MIMEText(body, "html")`) to produce nicer formatted messages.
* Add logging to a file to track which emails succeeded or failed.
* Use a templating engine or load personalized messages from the CSV.
* Add CLI flags (e.g., dry-run mode that prints messages instead of sending).

---

## Important Legal & Privacy Notes

* Only send emails to people you have permission to contact and where outreach is appropriate.
* Respect privacy and data protection rules (e.g., GDPR) as applicable in your jurisdiction.
* Follow platform rules (LinkedIn, etc.) — scraping or harvesting contact information without permission may violate terms.

---

## License

This project is provided as-is. Use it responsibly.

---

# 🚀 Autonomous Email Outreach Agent

A lightweight, single-user AI-powered agent that automates end-to-end recruiter outreach. It reads a CSV of contacts, generates personalized emails (LLM or template-based), sends them via Gmail SMTP, and logs all results for tracking.

This project focuses on practical agentic automation — no UI, no frameworks, just a clean workflow you can run locally.

---

## ✨ Features

### 1. CSV-Driven Outreach Workflow
- Accepts a simple CSV: `email, name, company`
- Validates entries and prepares them for sending
- Supports any number of contacts

### 2. AI-Backed Personalization (Optional)
- Uses OpenAI Chat Completion API to rewrite outreach emails
- Automatically falls back to template-based personalization if:
  - API quota is exceeded (429)
  - API key is missing or disabled
- Smooth hybrid behavior ensures reliability even without LLM access

### 3. Job Description Intelligence
- Automatically detects `job_description.txt` if present
- Summarizes JD once using LLM (key skills, responsibilities, highlights)
- Reuses summary across all contacts for efficient, consistent personalization
- Works perfectly fine without a JD (generic outreach mode)

### 4. Autonomous Email Sending via Gmail SMTP
- Uses Gmail App Password for secure SMTP authentication
- Sends each email with configurable rate-limiting (e.g., 10–30s per email)
- Prevents Gmail throttling and maintains deliverability
- Initializes SMTP once and reuses connection for efficiency

### 5. Failure-Aware Execution
Handles:
- Invalid email formats
- OpenAI quota errors (auto-disables LLM for remaining contacts)
- SMTP send errors
- Missing or malformed CSV entries
- Continues the workflow gracefully

### 6. Structured Logging
Every run updates `outreach_log.csv` with:

| email | name | company | status | timestamp | note |
|-------|------|---------|--------|-----------|------|

Statuses include:
- `PREPARED` (dry run)
- `SENT`
- `FAILED`
- `INVALID`

Useful for analytics and reply-tracking pipeline extensions.

---

## 🧠 Why This Counts as an Agent

Even without a UI, this script is an autonomous, tool-using, multi-step agent:

1. **Ingests data** (CSV + optional JD)
2. **Plans & optimizes** (summarizes JD once, reuses across contacts)
3. **Generates personalized messages** (LLM-powered or template fallback)
4. **Performs actions** through external tools (SMTP)
5. **Handles failures** & fallback pathways intelligently
6. **Logs state & outcomes** for every operation

This is core agentic behavior — far beyond a simple script.

---

## 📁 Project Structure
```
autobot/
├── outreach.py              # Main agent script
├── contacts.csv             # Sample input contacts
├── job_description.txt      # Optional JD for personalization
├── outreach_log.csv         # Generated logs (auto-created)
├── .env                     # Secrets (OpenAI key, Gmail app password)
└── README.md                # Project documentation
```

---

## 🔧 Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd autobot
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### 3. Install dependencies
```bash
pip install openai python-dotenv jinja2 tqdm
```

### 4. Configure `.env`
```env
OPENAI_API_KEY=your-openai-key   # Optional; will fall back to templates if missing or quota exceeded
SENDER_EMAIL=yourgmail@gmail.com
APP_PASSWORD=your_app_password
FROM_NAME="Your Name"
RATE_LIMIT_SECONDS=15
LOG_FILE=outreach_log.csv
USE_OPENAI=true
```

### 5. Prepare your contact CSV
```csv
email,name,company
recruiter@example.com,Jane Doe,Acme Corp
hiring@startup.io,John Smith,TechCo
...
```

### 6. (Optional) Add job description

Create `job_description.txt` in the project root:
```
We're looking for a Machine Learning Engineer with experience in:
- Python, PyTorch, TensorFlow
- Building and deploying LLM-based applications
- Vector databases and RAG systems
...
```

---

## ▶️ Running the Agent

### Dry run (no emails sent)
Generates drafts and logs them as `PREPARED`:
```bash
python outreach.py --csv contacts.csv
```

### Actual sending
Sends email via Gmail SMTP:
```bash
python outreach.py --csv contacts.csv --send
```

### Optional: Custom tone
```bash
python outreach.py --csv contacts.csv --tone formal
```

---

## 📬 How It Works

### User Workflow (What You Do)

1. **Prepare inputs:**
   - Create `contacts.csv` with recruiter details
   - (Optional) Add `job_description.txt` for JD-aware personalization

2. **Run the agent:**
   - Dry-run: `python outreach.py --csv contacts.csv`
   - Actual send: `python outreach.py --csv contacts.csv --send`

3. **Review logs:**
   - Check `outreach_log.csv` for delivery status

That's it! No manual copy-pasting or email client configuration needed.

---

### Internal Workflow (What the Agent Does)

Here's the complete autonomous execution flow:

#### **STEP 1: Load Environment Variables**
- Reads `.env` for SMTP credentials, OpenAI API key, rate limits
- Validates configuration before proceeding

#### **STEP 2: Read CSV**
- Loads all contacts from `contacts.csv`
- Validates email formats
- Skips invalid entries with logging

#### **STEP 3: Detect Job Description**
- Automatically checks if `job_description.txt` exists
- Loads JD text if present
- No user action required

#### **STEP 4: Summarize JD (One-Time Optimization)**
If JD exists, agent calls LLM once to extract:
- Key responsibilities
- Required skills
- What candidates should highlight

Example summary:
```
Key Points:
- Working with LLMs and autonomous agents
- Python, ML ops, vector databases
- Building production AI workflows
- Preference: hands-on AI project experience
```

**Why this matters:**
- Reduces token usage (summary reused for all contacts)
- Ensures consistent personalization
- Separates "understanding the job" from "writing emails"

#### **STEP 5: For Each Contact → Build Personalization Prompt**
For every recruiter, agent constructs a prompt:

**With JD:**
```
Using this JD summary + base template, generate a polished 
outreach email for:
Name: Jane Doe
Company: Microsoft
```

**Without JD:**
```
Improve this generic outreach template for this recruiter:
Name: Jane Doe
Company: Microsoft
```

#### **STEP 6: Generate Personalized Email**
Agent attempts LLM generation via OpenAI:

- **✅ Success:** Returns custom, polished email body
- **❌ Failure (429/quota):** 
  - Logs error
  - Disables LLM for remaining contacts
  - Falls back to Jinja template

**This is intelligent fallback behavior** — not a crash.

#### **STEP 7: Render Final Email**
- Inserts recruiter-specific fields: `{{ name }}`, `{{ company }}`
- If LLM succeeded → email already has JD-aware context
- If LLM failed → Jinja template completes basic personalization

#### **STEP 8: Initialize SMTP (Once)**
If `--send` flag is used:
```python
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login(SENDER_EMAIL, APP_PASSWORD)
```

Connection is reused for all emails (efficient).

#### **STEP 9: Send Email**
For each contact:
1. Create `EmailMessage` with From/To/Subject/Body
2. Call `smtp.send_message(msg)`
3. Wait `RATE_LIMIT_SECONDS` before next send
4. Prevents Gmail throttling

#### **STEP 10: Log Result**
After every email attempt, agent logs:
```csv
email,name,company,status,timestamp,note
jane@example.com,Jane Doe,Acme Corp,SENT,2025-01-15 10:23:45,Success
invalid@,Bad Name,FailCo,INVALID,2025-01-15 10:23:46,Invalid email format
john@startup.io,John Smith,TechCo,FAILED,2025-01-15 10:24:01,SMTP timeout
```

**Why logging matters:**
- Verifiability and audit trail
- Recovery from failed runs
- Foundation for reply-tracking features

#### **STEP 11: Cleanup & Exit**
- Closes SMTP connection gracefully: `smtp.quit()`
- Releases resources
- Exits with status summary

---

## 🔍 Key Agentic Behaviors

This agent demonstrates advanced autonomous capabilities:

| Behavior | Implementation |
|----------|----------------|
| **Intelligent Planning** | Summarizes JD once, reuses for efficiency |
| **Tool Usage** | SMTP for email, OpenAI API for generation |
| **Error Recovery** | Auto-fallback when LLM quota exceeded |
| **State Management** | Persistent logging across runs |
| **Resource Optimization** | Single SMTP connection, rate limiting |
| **Self-Awareness** | Detects files automatically, validates inputs |

---

## 🛡 Security Notes

- Uses Gmail App Password (safer than real password)
- `.env` is excluded from Git via `.gitignore`
- Rate-limits sending to avoid account flags
- Does not store sensitive data outside local machine
- No hardcoded credentials in code

---

## 📊 Example Log Output

After running with `--send`:
```csv
email,name,company,status,timestamp,note
alice@bigcorp.com,Alice Johnson,BigCorp,SENT,2025-01-15 10:15:32,Success
bob@startup.io,Bob Williams,StartupIO,SENT,2025-01-15 10:15:47,Success
invalid@email,Carol,FailCo,INVALID,2025-01-15 10:15:48,Invalid email format
dave@tech.com,Dave Brown,TechCo,SENT,2025-01-15 10:16:02,Success
```

---

## 🚀 Future Enhancements (Easy to Expand)

This project can grow into a full agentic system:

- **Reply Detection:** IMAP-based inbox monitoring
- **Reply Classification:** LLM categorization (positive/neutral/negative)
- **Autonomous Follow-ups:** Generate follow-up emails based on reply sentiment
- **A/B Testing:** Multiple templates with performance tracking
- **Web Dashboard:** Real-time monitoring and analytics
- **Chrome Automation:** Scrape recruiter data from LinkedIn
- **Multi-JD Support:** Handle different roles in one run
- **Attachment Support:** Auto-attach resume/portfolio

---

## 🐛 Troubleshooting

### "SMTP Authentication Failed"
- Ensure you're using a Gmail App Password (not your regular password)
- Enable 2FA on your Google account first
- Generate app password at: https://myaccount.google.com/apppasswords

### "OpenAI Quota Exceeded"
- Agent will automatically fall back to templates
- Check your OpenAI usage at: https://platform.openai.com/usage
- Consider upgrading your plan or reducing contact list size

### "Invalid Email Format" in logs
- Check CSV for malformed email addresses
- Ensure no empty cells in email column

### Emails going to spam
- Reduce `RATE_LIMIT_SECONDS` (try 30-60)
- Warm up your Gmail account with manual sends first
- Avoid spammy language in templates

---

## 📄 License

MIT License - feel free to use and modify for your own outreach needs.

---

## 🤝 Contributing

Pull requests welcome! Please open an issue first to discuss major changes.

---

## ⚠️ Disclaimer

Use responsibly. Ensure compliance with anti-spam laws (CAN-SPAM, GDPR) and recipient consent requirements in your jurisdiction. This tool is designed for legitimate professional outreach only.

---

## 💡 Tips for Best Results

1. **Start with dry runs** to test personalization quality
2. **Use a dedicated Gmail account** for outreach (not your personal email)
3. **Keep contact lists under 50** per run to avoid Gmail limits
4. **Review generated emails** before first actual send
5. **Monitor `outreach_log.csv`** to track success rates
6. **Space out campaigns** (don't send 100 emails in one hour)

---

## 🎯 Real-World Use Cases

- Job seekers reaching out to recruiters
- Sales outreach to potential clients
- Partnership proposals to companies
- Event invitations to industry contacts
- Follow-up campaigns after networking events

---

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from post_logger import post_log

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")

# ✅ 이메일 전송 함수
def send_email_report():
    if not (EMAIL_USER and EMAIL_PASS and TO_EMAIL):
        print("❌ Email credentials missing. Skipping email.")
        return

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    subject = f"📝 Daily Blogger Post Summary – {today}"

    body = "Auto-post complete. Here's what was published today:\n\n"
    if not post_log:
        body += "(No posts were logged.)"
    else:
        body += "\n".join(post_log)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("📬 Email report sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

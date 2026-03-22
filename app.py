from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

import os

EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

    except Exception as e:
        print("EMAIL ERROR:", e)
        raise


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    subject = f"New Land/Lot Alert: {data.get('address', 'Unknown address')}"
    body = f"""
New Listing Detected:

Address: {data.get('address')}
Price: {data.get('price')}
Acreage: {data.get('acreage')}
MLS ID: {data.get('mls_id')}
Source: {data.get('source')}
Link: {data.get('url')}
"""

    send_email(subject, body)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

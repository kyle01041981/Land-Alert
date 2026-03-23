from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

import requests
import os

MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

def send_email(subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Land Alerts <mailgun@{MAILGUN_DOMAIN}>",
            "to": EMAIL_TO,
            "subject": subject,
            "text": body
        }
    )

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

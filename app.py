from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)

EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("EMAIL_PASS")

@app.route("/send", methods=["POST"])
def send_email():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    try:
        msg = MIMEText(f"""
New Contact Message

Name: {name}
Email: {email}
Phone: {phone}
Message:
{message}
""")

        msg["Subject"] = f"New Message from {name}"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully!"})

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to send email"}), 500


if __name__ == "__main__":
    app.run()
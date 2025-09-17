from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Your Gmail and App Password
EMAIL_ADDRESS = "sarkarhimadri568@gmail.com"
EMAIL_PASSWORD = "uosr ncny bxin oqyc"   # your generated App Password

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"success": False, "message": "All fields are required!"}), 400

        # Create email for YOU (portfolio owner)
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS   # you receive the message
        msg["Subject"] = f"Portfolio Contact from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail and send
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

        # Confirmation email back to visitor
        confirm = MIMEMultipart()
        confirm["From"] = EMAIL_ADDRESS
        confirm["To"] = email
        confirm["Subject"] = "Thanks for contacting me!"

        confirm_body = (
            f"Hi {name},\n\n"
            f"Thanks for reaching out through my portfolio website. "
            f"I’ll get back to you soon.\n\nBest regards,\nHimadri"
        )
        confirm.attach(MIMEText(confirm_body, "plain"))

        server.send_message(confirm)
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully!"}), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

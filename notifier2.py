import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import resource_path

userDB = resource_path("db/users.db")

def get_family_contacts(user_email):
    conn = sqlite3.connect(userDB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, family1_name, family1_email, family2_name, family2_email 
        FROM users WHERE email = ?
    """, (user_email,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "user_name": result[0],
            "family1": {"name": result[1], "email": result[2]},
            "family2": {"name": result[3], "email": result[4]}
        }
    return {}

def send_email_alert(to_email, subject, message):
    try:
        sender_email = "dms.Alerts360@gmail.com"
        app_password = "xxxx xxxx xxxx xxxx"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def send_drowsiness_alerts(user_email):
    contacts = get_family_contacts(user_email)
    user_name = contacts.get("user_name", user_email.split("@")[0])

    subject = " Driver Drowsiness Alert - Immediate Attention Required!"

    for key in ["family1", "family2"]:
        contact = contacts.get(key)
        if contact and contact["email"]:
            message = f"""
Dear {contact['name']},

This is an automated safety alert from the DriCare360 Driver Monitoring System.

Your loved one, {user_name}, has shown signs of severe drowsiness or potential sleep while driving. The system has detected prolonged eye closure or inactivity, which could be extremely dangerous if they're currently on the road.

Immediate Action Recommended:
Please try to reach them and ensure their safety. It's strongly advised they stop driving and take a rest if needed.

Stay safe,
- The DriCare360 System
""".strip()

            print(f"Sending email to: {contact['email']}")
            send_email_alert(contact["email"], subject, message)

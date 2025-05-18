# def send_email(message):
#     print(f"📧 Email Sent: {message}")
#     return True
# def send(user_id: str, message: str):
#     print(f"Email sent to {user_id}: {message}")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# You can move these to environment variables or config later
EMAIL_ADDRESS = "11e18ishamittal@gmail.com"  # replace with your Gmail
EMAIL_PASSWORD = "xxwoeprlwtytqqla"   # replace with your app password

def send_email(user_id: str, message: str):
    try:
        recipient = user_id  # assuming user_id is an email for email type

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = "Notification Service Email"
        
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

import jwt
import datetime
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SECRET_KEY = os.environ.get('JWT_SECRET', 'super_secret_cyberguard_key_2026')

# Email config (Environment Variables should be set, otherwise it mocks)
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD') # E.g., Gmail App Password

def generate_jwt(user_id, email, name):
    """Generate a JWT token for standard sessions."""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id),
        'email': email,
        'name': name
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def generate_reset_code(length=6):
    """Generate a random 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=length))

def send_reset_email(to_email, reset_code):
    """
    Sends the reset code via email using smtplib if credentials are set.
    Otherwise, simply prints the code to the terminal for mock/hackathon purposes.
    """
    if SENDER_EMAIL and SENDER_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = 'CyberGuard Password Reset'

            body = f"Hello,\n\nYour CyberGuard password reset code is: {reset_code}\n\nIf you did not request this, please ignore this email."
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, to_email, text)
            server.quit()
            print(f"INFO: Reset email sent to {to_email}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to send real email: {e}")
            print(f"MOCK: Printing code for testing >> Email:{to_email} | Code:{reset_code}")
            return True
    else:
        # MOCK SENDING (Graceful fallback)
        print("="*40)
        print("MOCK EMAIL SENDER ACTIVATED")
        print("Because SENDER_EMAIL and SENDER_PASSWORD env vars are not set.")
        print(f"To: {to_email}")
        print(f"Subject: CyberGuard Password Reset")
        print(f"Body: Hello,\n\nYour CyberGuard password reset code is: {reset_code}\n\nIf you did not request this, please ignore this email.")
        print("="*40)
        print("="*40)
        return True

def send_scan_report_email(to_email, scan_type, risk_level, score, reasons):
    """
    Sends a summary of the scan results to the user's email.
    """
    if SENDER_EMAIL and SENDER_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = f'CyberGuard Alert: {risk_level} {scan_type} Detected'

            reasons_text = "\n- ".join(reasons)
            
            body = f"Hello,\n\nYou recently performed a {scan_type} scan on CyberGuard.\n\n"
            body += f"Here are your results:\n"
            body += f"Risk Level: {risk_level}\n"
            body += f"Safety Score: {score}/100\n\n"
            if reasons:
                body += f"Reasons Flagged:\n- {reasons_text}\n\n"
            
            body += "Please stay safe online,\nThe CyberGuard Team"
            
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, to_email, text)
            server.quit()
            print(f"INFO: Scan report email sent to {to_email}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to send scan report email: {e}")
            return False
    else:
        # Mocking for local dev without credentials
        print(f"MOCK EMAIL: Would have sent scan report to {to_email} (Risk: {risk_level}, Score: {score})")
        return True

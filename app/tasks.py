from .celery_config import celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from .celery_config import celery
from app.models import User
from flask import url_for
import pdfkit
from datetime import datetime, date
from app.models import User

logging.basicConfig(level=logging.INFO)

@celery.task
def send_login_reminder(subject, body):
    try:
        logging.info("Task send_login_reminder started")
        
        today = date.today()
        not_login_today = [user.Email for user in User.query.filter(
            User.Email.isnot(None),
            User.lastLogin != today
        ).all()]

        sender_email = 'putYourEmailHere@gmail.com'
        sender_password = 'putYourPasswordhere'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient_email in not_login_today:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)

        server.quit()
        logging.info("Task send_login_reminder completed")
    except Exception as e:
        logging.error(f"Error in send_login_reminder: {e}")

@celery.task
def send_pdf_to_multiple_users(pdf_path, subject, body):
    try:
        logging.info("Task send_pdf_to_multiple_users started")
        
        recipient_emails = [user.Email for user in User.query.filter(User.Email.isnot(None)).all()]
        sender_email = 'putYourEmailHere@gmail.com'
        sender_password = 'putYourPasswordhere'

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(pdf_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_path)}")
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient_email in recipient_emails:
            msg['To'] = recipient_email
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)

        server.quit()
        logging.info("Task send_pdf_to_multiple_users completed")
    except Exception as e:
        logging.error(f"Error in send_pdf_to_multiple_users: {e}")

@celery.task
def send_pdf_to_users(pdf_path, recipient_email, subject, body):
    try:
        logging.info("Task send_pdf_to_users started")
        
        sender_email = 'putYourEmailHere@gmail.com'
        sender_password = 'putYourPasswordhere'

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(pdf_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_path)}")
        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        attachment.close()
        
        logging.info("Task send_pdf_to_users completed")
    except Exception as e:
        logging.error(f"Error in send_pdf_to_users: {e}")

@celery.task
def pdfReport():
    users = User.query.all()
    for user in users:
        user_id = user.id
        email = user.email
        stats_url = url_for('userStats', _external=True) + f"?user_id={user_id}"
        try:
            pdf_path = f'Mislinious/Stats_{user_id}.pdf'
            pdfkit.from_url(stats_url, pdf_path)
            send_pdf_to_users(pdf_path, email, 'Your Monthly Report', 'Here is your monthly report.')
        except Exception as e:
            logging.error(f"Error generating or sending PDF for user {user_id}: {e}")
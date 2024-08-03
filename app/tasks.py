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

logging.basicConfig(level=logging.INFO)

@celery.task
def send_pdf_to_users(pdf_path, recipient_email, subject, body):
    try:
        logging.info("Task send_pdf_to_users started")
        
        sender_email = 'gnspdc@gmail.com'
        sender_password = 'bicgpthxanxunafk'

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

from .celery_config import celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# @celery.task
# def send_pdf_to_users(pdf_path, recipient_email, subject, body):
#     sender_email = 'gnspdc@gmail.com'
#     sender_password = 'bicgpthxanxunafk'

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
#     attachment = open(pdf_path, "rb")
#     part = MIMEBase('application', 'octet-stream')
#     part.set_payload(attachment.read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_path)}")
#     msg.attach(part)
#     text = msg.as_string()

#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, recipient_email, text)
#     server.quit()
#     attachment.close()

import logging
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

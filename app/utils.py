import os
import datetime

def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def update_issue_status(book_issues):
    today = datetime.date.today().strftime('%Y-%m-%d')
    for book_issue in book_issues:
        if book_issue.IssueStatus == 'Approved' and book_issue.IssueDate < today:
            book_issue.IssueStatus = 'Rejected'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_pdf_to_users(pdf_path,recipient_email, subject, body):
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

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from your_app import db
# from models import User


# def get_all_user_emails():
#     users = User.query.all()
#     return [user.Email for user in users]

# def send_pdf_to_all_users(pdf_path, subject, body):
#     sender_email = 'gnspdc@gmail.com'
#     sender_password = 'bicgpthxanxunafk'

#     recipient_emails = get_all_user_emails()

#     for recipient_email in recipient_emails:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = recipient_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))
#         attachment = open(pdf_path, "rb")
#         part = MIMEBase('application', 'octet-stream')
#         part.set_payload(attachment.read())
#         encoders.encode_base64(part)
#         part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_path)}")
#         msg.attach(part)
#         text = msg.as_string()

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipient_email, text)
#         server.quit()
#         attachment.close()
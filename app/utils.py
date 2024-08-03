# Define your utility functions or helper functions here
import os
import datetime
import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from app.models import User
from flask import url_for

def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def update_issue_status(book_issues):
    today = datetime.date.today().strftime('%Y-%m-%d')
    for book_issue in book_issues:
        if book_issue.IssueStatus == 'Approved' and book_issue.IssueDate < today:
            book_issue.IssueStatus = 'Rejected'

def pdfReport():
    try:
        pdfkit.from_url('http://127.0.0.1:5000/userStats', 'Mislinious/Stats.pdf')
    except:
        pdfkit.from_url('http://127.0.0.1:5000/adminStats', 'Mislinious/Stats.pdf')
    try:
        pdfkit.from_url('http://127.0.0.1:5000/myBooks', 'Mislinious/Books.pdf')
    except:
        pdfkit.from_url('http://127.0.0.1:5000/requestedBooks', 'Mislinious/Books.pdf')


def pdfReports():
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
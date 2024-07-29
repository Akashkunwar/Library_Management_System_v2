# from celery import Celery
# import pdfkit
# from utils import send_pdf_to_all_users

# celery = Celery('tasks', broker='redis://localhost:6379/0')
# celery.config_from_object('celeryconfig')

# @celery.task
# def send_monthly_stats():
#     pdfkit.from_url('http://127.0.0.1:5000/adminStats', 'app/test.pdf')
#     subject = "Monthly Stats Report"
#     body = "Please find attached the monthly stats report."
#     send_pdf_to_all_users('app/test.pdf', subject, body)


import pdfkit
from .utils import send_pdf_to_all_users
from .celery import celery

@celery.task
def send_monthly_stats():
    pdfkit.from_url('http://127.0.0.1:5000/adminStats', 'app/test.pdf')
    subject = "Monthly Stats Report"
    body = "Please find attached the monthly stats report."
    recipient_email = 'gnspda@gmail.com'
    send_pdf_to_all_users('app/test.pdf', recipient_email, subject, body)

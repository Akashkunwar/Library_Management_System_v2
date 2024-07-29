# from celery.schedules import crontab
# from .tasks import send_pdf_to_users

# celery.conf.beat_schedule = {
#     'send-pdf-every-month': {
#         'task': 'app.tasks.send_pdf_to_users',
#         'schedule': crontab(day_of_month=1, hour=0, minute=0),  # 1st of every month at midnight
#         'args': ['app/test.pdf', 'gnspda@gmail.com', 'Monthly Report', 'Please find the attached PDF.']
#     },
# }

from celery.schedules import crontab
from .tasks import send_pdf_to_users

celery.conf.beat_schedule = {
    'send-pdf-every-minute-for-5-minutes': {
        'task': 'app.tasks.send_pdf_to_users',
        'schedule': crontab(minute='*/1'),  # Every minute
        'args': ['app/test.pdf', 'gnspda@gmail.com', 'Testing Subject', 'Testing Body']
    },
}

from celery.schedules import crontab
from .celery_config import celery
from .tasks import send_pdf_to_users

# celery.conf.beat_schedule = {
#     'send-pdf-every-minute-for-5-minutes': {
#         'task': 'app.tasks.send_pdf_to_users',
#         'schedule': crontab(minute='*/1'),
#         'args': ['Mislinious/Stats.pdf', 'gnspda@gmail.com', 'Testing Subject', 'Testing Body']
#     },
# }

# celery.conf.timezone = 'UTC'

celery.conf.beat_schedule = {
    'send-pdf-on-1st-of-month-8am': {
        'task': 'app.tasks.send_pdf_to_users',
        'schedule': crontab(minute=0, hour=8, day_of_month=1),
        'args': ['Mislinious/Stats.pdf', 'gnspda@gmail.com', 'Monthly Report', 'Here is the monthly report.']
    },
}

celery.conf.timezone = 'UTC'
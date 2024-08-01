from celery.schedules import crontab
from .celery_config import celery
from .tasks import send_pdf_to_users

celery.conf.beat_schedule = {
    'send-pdf-every-minute-for-5-minutes': {
        'task': 'app.tasks.send_pdf_to_users',
        'schedule': crontab(minute='*/1'),
        'args': ['Mislinious/Stats.pdf', 'gnspda@gmail.com', 'Testing Subject', 'Testing Body']
    },
}

celery.conf.timezone = 'UTC'

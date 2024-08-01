from celery import Celery

celery = Celery('app', broker='redis://localhost:6379/0')

celery.conf.update(
    result_backend='redis://localhost:6379/0',
    timezone='UTC',
)

import app.celery_schedule
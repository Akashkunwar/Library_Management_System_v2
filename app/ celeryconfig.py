# from celery.schedules import crontab

# CELERYBEAT_SCHEDULE = {
#     'send-monthly-stats': {
#         'task': 'tasks.send_monthly_stats',
#         'schedule': crontab(day_of_month=1, hour=0, minute=0),
#     },
# }

# CELERY_TIMEZONE = 'UTC'

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'send-monthly-stats': {
        'task': 'app.task.send_monthly_stats',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}

CELERY_TIMEZONE = 'UTC'

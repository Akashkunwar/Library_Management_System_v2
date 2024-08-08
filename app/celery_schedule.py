from celery.schedules import crontab
from .celery_config import celery
from .tasks import send_pdf_to_users, send_pdf_to_multiple_users, send_login_reminder

celery.conf.beat_schedule = {
    'send-pdf-to-single-user-on-1st-of-month-8am': {
        'task': 'app.tasks.send_pdf_to_users',
        'schedule': crontab(minute=0, hour=8, day_of_month=1),
        'args': ['Mislinious/Stats.pdf', 'gnspda@gmail.com', 'Monthly Report', 'Here is the monthly report.']
    },

    'send-pdf-to-multiple-users-on-1st-of-month-8am': {
        'task': 'app.tasks.send_pdf_to_multiple_users',
        'schedule': crontab(minute=0, hour=8, day_of_month=1),
        'args': [
            'Mislinious/Stats.pdf',
            'Monthly Report',
            'Here is the monthly report.'
        ]
    },

    'send-login-reminder-daily-9pm': {
        'task': 'app.tasks.send_login_reminder',
        'schedule': crontab(minute=0, hour=21),
        'args': [
            'Daily Login Reminder', 
            'Please login.'
        ]
    },
}

celery.conf.timezone = 'UTC'


# from celery.schedules import crontab
# from .celery_config import celery
# from .tasks import send_pdf_to_users, send_pdf_to_multiple_users, send_login_reminder
# from sqlalchemy import func, and_, or_, desc
# from datetime import datetime, date
# from app.models import User
# def emails():
#     email_list = [user.Email for user in User.query.filter(User.Email.isnot(None)).all()]
#     return email_list

# def notLoginToday():
#     today = date.today()
#     notLoginToday = [user.Email for user in User.query.filter(User.Email.isnot(None),User.lastLogin != today).all()]
#     return notLoginToday

# celery.conf.beat_schedule = {
#     'send-pdf-to-single-user-on-1st-of-month-8am': {
#         'task': 'app.tasks.send_pdf_to_users',
#         'schedule': crontab(minute=0, hour=8, day_of_month=1),
#         'args': ['Mislinious/Stats.pdf', 'gnspda@gmail.com', 'Monthly Report', 'Here is the monthly report.']
#     },

#     'send-pdf-to-multiple-users-on-1st-of-month-8am': {
#         'task': 'app.tasks.send_pdf_to_multiple_users',
#         'schedule': crontab(minute=0, hour=8, day_of_month=1),
#         'args': [
#             'Mislinious/Stats.pdf',
#             emails(),
#             'Monthly Report', 
#             'Here is the monthly report.'
#         ]
#     },

#     'send-login-reminder-daily-9pm': {
#         'task': 'app.tasks.send_login_reminder',
#         'schedule': crontab(minute=0, hour=21),
#         'args': [
#             notLoginToday(),
#             'Daily Login Reminder', 
#             'Please login.'
#         ]
#     },
# }

# celery.conf.timezone = 'UTC'


# celery.conf.beat_schedule = {
#     'send-pdf-every-minute-for-5-minutes': {
#         'task': 'app.tasks.send_pdf_to_users',
#         'schedule': crontab(minute='*/1'),
#         'args': ['Mislinious/Stats.pdf', 'gnspda@gmail.com', 'Testing Subject', 'Testing Body']
#     },
# }

# celery.conf.timezone = 'UTC'

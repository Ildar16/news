import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news1.settings')

app = Celery('news1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'sendmail_every_week': {
        'task': 'weekly_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='sunday'),
    },
}

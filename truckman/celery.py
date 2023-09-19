from __future__ import absolute_import, unicode_literals 
import os
from celery import Celery
from celery.schedules import crontab 


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truckman.settings')

app = Celery('truckman')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['truckman'])

app.conf.beat_schedule = {
    'hello_engima': {
        'task': 'truckman.tasks.hello_engima',
        'schedule': crontab(minute='*'),
    },
} 
from __future__ import absolute_import
import os

from celery import Celery
from django.conf import settings
# set the default Django settings module for the 'celery' program.




__all__ = [
    'celery',
    'QueueOnce',
]
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autobets.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
import configurations

configurations.setup()

app = Celery('autobets')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.ONCE = settings.CELERY_ONCE
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ToastmastersFSA.settings')

app = Celery('ToastmastersFSA')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


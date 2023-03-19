import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sellit_api.settings.development')

project = "sellit_api"
app = Celery(f"{project}_{os.getenv('DJANGO_SETTINGS_MODULE').split('.')[-1]}")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {

}

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_oauth2_emailverifier.settings")

celery = Celery("django_oauth2_emailverifier")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
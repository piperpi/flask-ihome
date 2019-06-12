# coding:utf-8
from celery import Celery
from ihome.tasks import config

celery_app = Celery('ihome')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks(['ihome.tasks.sms'])



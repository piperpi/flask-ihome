from ihome.tasks.main import celery_app
from ihome.libs.yuntongxun.SendTemplateSMS import sendTemplateSMS


@celery_app.task
def send_sms(to, datas, tempId):
    sendTemplateSMS(to, datas, tempId)

from __future__ import absolute_import
from  __future__ import  absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
app= Celery('backend')
app.conf.enable_utc=False
app.config_from_object(settings,namespace='CELERY')


#CELERY BEAT 
app.conf.beat_schedule={

}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
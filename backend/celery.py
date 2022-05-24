
from  __future__ import  absolute_import , unicode_literals
import os
from celery import Celery
from django.conf import settings
from pytz import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
app= Celery('backend')
app.conf.enable_utc=False

app.conf.update(timezone ='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')


#CELERY BEAT 


# app.conf.beat_schedule={
#     "schedule_taskss" :{
#         "task":"send_review_email_task" ,
#         "schedule":1.0 , 
#         "args":(1000,1000) , 

#     }
# }

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
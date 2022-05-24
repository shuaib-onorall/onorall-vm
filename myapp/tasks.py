from celery import shared_task
from .models import detail
@shared_task
def test_func(x , y):
    
    return x+y

@shared_task
def latest_to_old(videoid):
    obj = detail.objects.get(videoid=videoid)
    print('tasks runningggg--------')
    obj.status='Old'
    obj.save()
    
    return F'VideoId : {obj.videoid} has  goes from Latest To Old'
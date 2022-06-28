from pickle import TRUE
from celery import shared_task
from .models import LikeModel, detail , Support, workbaseinfo


@shared_task
def test_func(x , y):
    
    return x+y



@shared_task
def publish_time_celery_task(videoid):
    obj = detail.objects.get(videoid=videoid)
    if obj.ready_to_publish is False:
        obj.ready_to_publish=True
        print('working...............................')
        obj.save()
    
    return F'VideoId : {obj.videoid} has gone to ready_to_pulish=True '



@shared_task
def popular_videos():
    for workbase in workbaseinfo.objects.all():
        if workbase.workbase_supporter.count() >= 10:
            print(workbase.userid)
            for video in detail.objects.filter(user_id = workbase.userid):
                LikeModel.objects.filter(videos = video.id).videos.count()
              


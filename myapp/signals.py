from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from .models import *
from channels.layers import get_channel_layer

from django.core.cache import cache

from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver
from .models import detail
from django.http import HttpRequest
from django.utils.cache import get_cache_key


from .tasks import publish_time_celery_task
 
# for automatic change status latest to old
@receiver(post_save, sender=detail)
def create_profile(sender, instance, created, **kwargs):
    
    if instance.publish_time is not None:
        publish_time_celery_task.apply_async(args=[instance.videoid], countdown = int(instance.publish_time))



# for update cache when new video uploaded 
@receiver(post_save, sender=detail)
def clear_cache(sender, instance, **kwargs):
    cache.clear()
    
    
    

@receiver(post_delete, sender=detail)
def clear_cache(sender, instance, **kwargs):
    cache.delete('/general')
    cache.clear()





@receiver(post_save, sender=Notification, dispatch_uid='connect_comment')
def notification(sender, instance, **kwargs):
    group_name = 'gossip'
    message = {
        'notice': instance.notice,   #inside the message we put the instancve that we want 
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'text': message
        }
    )


@receiver(post_save,sender=connect_comment)
def comment(sender,instance,created,**kwargs):
    if created:
        new_notice= Notification.objects.create(notice=instance.post_comment)
        new_notice.save()

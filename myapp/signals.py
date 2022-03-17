from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from .models import *
from channels.layers import get_channel_layer

@receiver(post_save,sender=Notification)
def new_notice(sender,instance,created,**kwargs):
    if created:
        channel_layer=get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'gossip',{
                "type":"notice.gossip",
                'event':'new notice',
                'notice':instance.notice
            }
        )


from django.dispatch import Signal

__all__ = (
    'object_liked',
    'object_unliked'
)


object_liked = Signal(providing_args=["like", "request"])
object_unliked = Signal(providing_args=["object", "request"])

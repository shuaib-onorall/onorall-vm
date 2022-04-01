from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from .models import *
from channels.layers import get_channel_layer

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

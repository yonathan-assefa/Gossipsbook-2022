from .models import Notifications
from gossips.models import GossipsModel, Comments, Reply
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



@receiver(signal=post_save, sender=Reply)
def create_notification_for_replying(sender, instance, created, **kwargs):
    if created:
        reply_user = instance.user
        comment_user = instance.comment.author

        if comment_user == reply_user:
            return

        msg = f"{reply_user.username} replied to your Comment..."
        obj = Notifications.objects.create(user=comment_user, message=msg)
        return obj


@receiver(signal=post_save, sender=Comments)
def create_notification_for_commenting(sender, instance, created, **kwargs):
    if created:
        user = instance.gossip.author
        comment_user = instance.author
        if comment_user == user:
            return 

        msg = f"{comment_user.username} Commented not your Gossip..."
        obj = Notifications.objects.create(user=user, message=msg)
        return obj



@receiver(signal=post_save, sender=Notifications)
def websocket_not(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    username = instance.user.username
    chat_room = f"notification_room_{username}"
    instance_data = instance.message
    print("\n")
    print("\n")
    print("From Signal", chat_room)

    async_to_sync(channel_layer.group_send)(
        chat_room,
        {
            "type": "send.notification",
            # "event": "Hello Signal World...",
            "data": instance_data
        }
    )

    print("\n")
    print("\n")

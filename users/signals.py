from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, Friend
from django.contrib.auth.models import User


@receiver(signal=post_save, sender=FriendRequest)
def can_a_friend_model_be_created(sender, instance, created, **kwargs):
    username1 = instance.to_user.username
    username2 = instance.sent_by_user.username
    print("Inside Signals")
    if instance.accepted == True:
        qs = Friend.objects.can_a_friend_model_be_created(user1_username=username1, user2_username=username2)
        if qs == True:
            user1 = User.objects.get(username=username1)
            user2 = User.objects.get(username=username2)
            obj = Friend.objects.create(user1=user1, user2=user2)
            return obj
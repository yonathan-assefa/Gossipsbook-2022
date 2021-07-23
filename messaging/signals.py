# from .models import Notifications
# from gossips.models import GossipsModel, Comments, Reply, User
# from users.models import Profile, CircleFollower
# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# @receiver(signal=post_save, sender=CircleFollower)
# def create_notification_for_circle_follower(sender, instance, created, **kwargs):
#     if created:
#         follower_user = instance.user
#         following_user = instance.circle.user
#         message = f"{follower_user.username} started Following Your Circle..."
#         obj = Notifications.objects.create(user=following_user, message=message)
#         return obj


# @receiver(signal=m2m_changed, sender=Profile.followers.through)
# def create_notification_for_follower(sender, instance, action, **kwargs):
#     if action == "pre_add":
#         user_following = sender.objects.last().user
#         user_main = instance.user
#         message = f"{user_following.username} has Started Following You..."
#         obj = Notifications.objects.create(user=user_main, message=message)
#         return obj


# @receiver(signal=m2m_changed, sender=GossipsModel.true.through)
# def create_notification_for_true(sender, instance, action, **kwargs):
#     # print(sender.objects.last().user, instance, action)
#     # print(pk_set)
#     # print(kwargs.values())
#     # print(**kwargs["pk_set"])
#     if action == "pre_add":
#         user = instance.author
#         # chat_user = User.objects.get(username="chat_user")
#         message = f"{sender.objects.last().user} Has voted True in your Gossip..."
#         obj = Notifications.objects.create(user=user, message=message)
#         return obj


# @receiver(signal=m2m_changed, sender=GossipsModel.false.through)
# def create_notification_for_true(sender, instance, action, **kwargs):
#     if action == "pre_add":
#         user = instance.author
#         message = f"{sender.objects.last().user} Has voted False in your Gossip..."
#         obj = Notifications.objects.create(user=user, message=message)
#         return obj


# # @receiver(signal=post_save, sender=GossipsModel)
# # def update_user_feed(sender, instance, created, **kwargs):
# #     if created:
# #         user = instance.author
# #         channel_layer = get_channel_layer()

# #         qs = user.user1_frnds.all()
# #         for i in qs:
# #             chat_room = f"notification_room_{i.user2.username}"
# #             async_to_sync(channel_layer.group_send)(
# #             chat_room,
# #             {
# #                 "type": "send.notification",
# #                 # "event": "Hello Signal World...",
# #                 "data": "New Gossips Available"
# #             }
# #         )
        
# #         qs = user.user2_frnds.all()
# #         for i in qs:
# #             chat_room = f"notification_room_{i.user1.username}"
# #             async_to_sync(channel_layer.group_send)(
# #             chat_room,
# #             {
# #                 "type": "send.notification",
# #                 # "event": "Hello Signal World...",
# #                 "data": "New Gossips Available"
# #             }
# #         )


# @receiver(signal=post_save, sender=Reply)
# def create_notification_for_replying(sender, instance, created, **kwargs):
#     if created:
#         reply_user = instance.user
#         comment_user = instance.comment.author

#         if comment_user == reply_user:
#             return

#         msg = f"{reply_user.username} replied to your Comment..."
#         obj = Notifications.objects.create(user=comment_user, message=msg)
#         return obj


# @receiver(signal=post_save, sender=Comments)
# def create_notification_for_commenting(sender, instance, created, **kwargs):
#     if created:
#         user = instance.gossip.author
#         comment_user = instance.author
#         if comment_user == user:
#             return 

#         msg = f"{comment_user.username} Commented not your Gossip..."
#         obj = Notifications.objects.create(user=user, message=msg)
#         return obj


# @receiver(signal=post_save, sender=Notifications)
# def websocket_not(sender, instance, created, **kwargs):
#     channel_layer = get_channel_layer()
#     username = instance.user.username
#     chat_room = f"notification_room_{username}"
#     instance_data = instance.message
#     print("\n")
#     print("From Signal", chat_room)

#     async_to_sync(channel_layer.group_send)(
#         chat_room,
#         {
#             "type": "send.notification",
#             # "event": "Hello Signal World...",
#             "data": instance_data
#         }
#     )

#     print("\n")

from channels.consumer import AsyncConsumer
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from .models import Notifications, ChatingRoomMessage, ChatingRoom
from channels.db import database_sync_to_async
import json
import asyncio
from django.contrib.auth.models import User


class ChatMessageConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("[ CONNECTED ] ", event)
        user = self.scope["user"]
        if not user.is_authenticated:
            print("Un-Authenticated")
            await self.send({
                "type": "websocket.disconnect",
            })
            return
        
        await self.send({
            "type": "websocket.accept",
        })

        user2_username = self.scope["url_route"]["kwargs"]["username"]
        chat_room_obj = await self.get_chatroom_from_db(user.username, user2_username)
        self.chat_room = f"room_{chat_room_obj.id}"
        print("Added")

        print(chat_room_obj)

        await self.channel_layer.group_add(
            f"room_{chat_room_obj.id}",
            self.channel_name
        )

    async def websocket_receive(self, event):
        print("[ RECEIVED ] ", event)
        message_dict = event["text"]
        data = json.loads(message_dict)
        user_sent_username = data["user"]
        message_sent = data["message"]

        print(user_sent_username, message_sent)

        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "send_text_message_to_room",
                "data": json.dumps({"msg": message_sent, "user": user_sent_username})
            }
        )

        user1 = self.scope["user"]
        user2 = self.scope["url_route"]["kwargs"]["username"]
        other_user = get_object_or_404(User, username=user2)
        sent_by_user = user1

        if user1.username != user_sent_username:
            sent_by_user = other_user
            other_user = user1

        await self.create_chat_message(sent_user=sent_by_user, to_user=other_user, 
                                                                message=message_sent)

    async def websocket_disconnect(self, event):
        print("[ DIS-CONNECTED ] ", event)

    async def send_text_message_to_room(self, event):
        # event = event["data"]
        # msg = event["msg"]
        # user_sent = event["user"]
        
        # data = json.dumps({
        #     "message": msg,
        #     "user": user_sent
        # })
        
        data = event["data"]
        await self.send({
            "type": "websocket.send",
            "text": data
        })

    @database_sync_to_async
    def get_chatroom_from_db(self, username1, username2):
        obj = ChatingRoom.objects.get_or_create_room(username1, username2)
        return obj

    @database_sync_to_async
    def create_chat_message(self, sent_user, to_user, message):
        chat_room_id = str(self.chat_room).split("room_")[1]
        print(chat_room_id)
        obj = get_object_or_404(ChatingRoom, id=chat_room_id)
        obj.ch_messages.create(user1=sent_user, user2=to_user, sent_by_user=sent_user, 
                                                                        message=message)
        return obj



class NotificationConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("CONNTECTED -> ", event)
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.send({
                "type": "websocket.disconnect"
            })
            return 

        username = user.username
        
        chat_room = f"notification_room_{username}"
        self.chat_room = chat_room
        print(chat_room)
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })


    async def websocket_receive(self, event):
        print("RECEIVED -> ", event)
        data = event["text"]

        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "send_notification",
                "data": data
            }
        )

    async def send_notification(self, event):
        data = event["data"]
        print(data)
        await self.send({
            "type": "websocket.send",
            "text": data,
        })

    async def websocket_disconnect(self, event):
        print("DIS-CONNTECTED -> ", event)




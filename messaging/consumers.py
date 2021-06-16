from channels.consumer import AsyncConsumer
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from .models import Notifications, ChatingRoomMessage, ChatingRoom
from channels.db import database_sync_to_async
import json
import asyncio


class ChatMessageConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("[ CONNECTED ] ", event)
        user = self.scope["user"]
        if user.is_authenticated:
            print("Authenticated")
            raise Http404()
        
        await self.send({
            "type": "websocket.accept",
        })

        user2_username = self.scope["url_route"]["kwargs"]["username"]
        chat_room_obj = await self.get_chatroom_from_db(user.username, user2_username)
        self.chat_room = f"room_{chat_room_obj.id}"
        await self.channel_layer.group_add(
            f"room_{chat_room_obj.id}",
            self.channel_name
        )

    async def websocket_receive(self, event):
        print("[ RECEIVED ] ", event)

    async def websocket_disconnect(self, event):
        print("[ DIS-CONNECTED ] ", event)

    @database_sync_to_async
    def get_chatroom_from_db(self, username1, username2):
        obj = ChatingRoom.objects.get_or_create_room(username1, username2)
        return obj

    @database_sync_to_async
    def get_chatroom_by_id(self, id):
        obj = get_object_or_404(ChatingRoom, id=id)
        return obj
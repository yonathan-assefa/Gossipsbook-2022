from django.contrib import admin
from .models import ChatingRoom, ChatingRoomMessage, Notifications

admin.site.register(ChatingRoom)
admin.site.register(ChatingRoomMessage)
admin.site.register(Notifications)

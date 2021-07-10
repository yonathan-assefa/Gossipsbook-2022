from django.contrib import admin
from .models import Profile, Interests,  Circle, CircleInfo, CirclePhoto, Friend, FriendRequest

admin.site.register(Profile)
admin.site.register(Interests)
admin.site.register(Circle)
admin.site.register(CircleInfo)
admin.site.register(CirclePhoto)
admin.site.register(Friend)
admin.site.register(FriendRequest)

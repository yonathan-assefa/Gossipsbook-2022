from django.contrib import admin

# Register your models here.

from .models import Profile, Interests

admin.site.register(Profile)
admin.site.register(Interests)

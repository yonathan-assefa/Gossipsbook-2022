from django.contrib import admin
from .models import RestToken

class RestTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expired", "date_created")


admin.site.register(RestToken, RestTokenAdmin)
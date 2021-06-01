from django.contrib import admin
from .models import FalseInformation, RFRModel, FeedbackModel

# Register your models here.

@admin.register(FalseInformation)
class FalseInformationAdmin(admin.ModelAdmin):
    list_display = ['gossip', 'cheater']


@admin.register(RFRModel)
class RFRAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'post_title', 'reason', 'section']


@admin.register(FeedbackModel)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'message']

from django.contrib import admin

from .models import AnswersModel


@admin.register(AnswersModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'shares']

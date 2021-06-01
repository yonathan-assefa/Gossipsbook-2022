from django.contrib import admin

from .models import QuestionsModel, Tags

admin.site.register(Tags)


@admin.register(QuestionsModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}

from django.contrib import admin

from .models import CheatersModel, Tags, Comments

admin.site.register(Tags)


@admin.register(CheatersModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comments)
class PostAdmin(admin.ModelAdmin):
    list_display = ['cheater', 'author']


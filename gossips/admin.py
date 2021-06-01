from django.contrib import admin

from .models import GossipsModel, Tags, Comments

admin.site.register(Tags)


@admin.register(GossipsModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comments)
class PostAdmin(admin.ModelAdmin):
    list_display = ['gossip', 'author']

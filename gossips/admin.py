from django.contrib import admin

from .models import GossipsModel, Tags, Comments, Reply

admin.site.register(Tags)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "content", "date_updated")

admin.site.register(Reply, ReplyAdmin)

@admin.register(GossipsModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comments)
class PostAdmin(admin.ModelAdmin):
    list_display = ['gossip', 'author']

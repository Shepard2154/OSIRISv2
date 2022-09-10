from django.contrib import admin

from .models import *


admin.site.register(Replies)
admin.site.register(Likes)
admin.site.register(Hashtags)
admin.site.register(Profiles)


@admin.register(ActiveCeleryTasks)
class ActiveCeleryTasksAdmin(admin.ModelAdmin):
    readonly_fields = ('task_id', 'entities',)
    search_fields = ('name',)
    actions = None

    def has_add_permission(self, request, obj=None):
        return False


    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    search_fields = ('screen_name',)


@admin.register(Tweets)
class TweetsAdmin(admin.ModelAdmin):
    search_fields = ('author_screen_name',)
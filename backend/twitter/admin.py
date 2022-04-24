from django.contrib import admin

from .models import *


admin.site.register(TwitterUser)
admin.site.register(TwitterTweet)
admin.site.register(TwitterRelations)
admin.site.register(TwitterComments)
admin.site.register(TwitterLikes)
from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TwitterUser)
admin.site.register(TwitterTweet)
admin.site.register(TwitterRelations)
admin.site.register(TwitterComments)
admin.site.register(TwitterLikes)
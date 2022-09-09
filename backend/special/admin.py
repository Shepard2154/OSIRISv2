from django.contrib import admin

from .models import *


admin.site.register(Users)
admin.site.register(Tweets)
admin.site.register(Replies)
admin.site.register(Likes)
admin.site.register(Hashtags)
admin.site.register(Profiles)
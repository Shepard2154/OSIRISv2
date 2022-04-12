from django.urls import path, re_path
from django.conf.urls import url

from .views import *

from . import consumer

urlpatterns = [
    path('v1/person/<str:screen_name>/', DownloadPersonInfo.as_view()),
    path('v1/tweets/<str:screen_name>/', DownloadTweets.as_view()),
    path('v1/tweet/<int:tweet_id>/', V1_DownloadTweet.as_view()),
    path('statistics/<str:screen_name>/', CalculateTweetsStatistics.as_view()),

    path('ws/hashtag/', MessageSendAPIView.as_view()),

]

# websocket_urlpatterns = [
#     url(r'twitter/ws/hashtag/', consumer.ChatConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    re_path(r'twitter/ws/hashtag/', consumer.ChatConsumer.as_asgi()),
]
from django.urls import path

from .views import *


urlpatterns = [
    path('v1/tweet/<int:tweet_id>/', V1_DownloadTweetById.as_view()),
    path('v1/user/<str:screen_name>/', V1_DownloadUser.as_view()),
    path('v1/tweets/<str:screen_name>/', V1_DownloadTweetsFromPerson.as_view()),
    path('v1/likes/<str:screen_name>/', V1_DownloadLikesById.as_view()),

    path('v2/user/<str:screen_name>/', V2_DownloadUser.as_view()),
    path('v2/hashtags/', V2_DownloadTweetsByManyHashtags.as_view()),
    path('v2/all_hashtags/<int:max_count>/', V2_DownloadTweetsByLimit.as_view()),
    path('v2/comments/<str:screen_name>/<int:max_count>/', V2_DownloadCommentsByScreenName.as_view()),

    path('hashtags/setfromfile/', GetHashtagsFromFile.as_view()),

    path('monitoring/hashtags/', MonitoringHashtags.as_view()),
    path('monitoring/persons/', MonitoringUsers.as_view()),

    path('db/csv/', DatabaseToCSV.as_view()),
    path('db/hashtags/csv/', TweetsByHashtagToCSV.as_view()),
]
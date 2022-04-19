from django.urls import path

from .views import *

urlpatterns = [
    path('webdriver/hashtag/<str:hashtag_value>/<int:power>/', Webdriver_DownloadTweetsByHashtags.as_view()),

    path('v1/person/<str:screen_name>/', V1_DownloadPerson.as_view()),
    path('v1/tweets/<str:screen_name>/', V1_DownloadTweetsFromPerson.as_view()),
    path('v1/tweet/<int:tweet_id>/', V1_GetTweetById.as_view()),

    path('v2/person/<str:username>/', V2_DownloadPerson.as_view()),
    path('v2/hashtag/<str:hashtag_value>/<int:power>/', V2_DownloadTweetsByHashtags.as_view()),
    path('v2/hashtags/', V2_DownloadTweetsByManyHashtags.as_view()),

    path('statistics/<str:screen_name>/', CalculateUserStatistics.as_view()),

    
    path('hashtags/setfromfile/', GetHashtagsFromFile.as_view()),

    path('monitoring/hashtags/', Monitoring.as_view()),
]
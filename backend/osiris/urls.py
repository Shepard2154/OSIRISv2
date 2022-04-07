from django.urls import path
from .views import (
    UserCreateAPIView, 
    UserDetailAPIView, 
    UserUpdateAPIView, 
    UserDeleteAPIView, 
    UserListAPIView,
    UserRetrieveAPIView,
    RegistrationAPIView,
    LoginAPIView,
    Logout,
    DownloadUserInfo,
    DownloadTweets,

    CalculateTweetsStatistics,
)


urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', Logout.as_view()),

    path('user/create/', UserCreateAPIView.as_view(), name='create'),
    path('user/detail/<str:screen_name>/', UserRetrieveAPIView.as_view()),
    path('user/update/', UserUpdateAPIView.as_view()),
    path('user/delete/', UserDeleteAPIView.as_view()),
    path('user/list/', UserListAPIView.as_view()),

    path('person/<str:screen_name>/', DownloadUserInfo.as_view()),

    path('tweets/<str:screen_name>/', DownloadTweets.as_view()),

    path('statistics/<str:screen_name>/', CalculateTweetsStatistics.as_view()),
]

from django.urls import path
from django.contrib import admin
from .views import (
    UserCreateAPIView, 
    UserDetailAPIView, 
    UserUpdateAPIView, 
    UserDeleteAPIView, 
    UserListAPIView,
    RegistrationAPIView,
    LoginAPIView,
    download_tweets
)


urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='create'),
    path('user/detail/', UserDetailAPIView.as_view()),
    path('user/update/', UserUpdateAPIView.as_view()),
    path('user/delete/', UserDeleteAPIView.as_view()),
    path('user/list/', UserListAPIView.as_view()),
    path('person/', download_tweets.as_view()),
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]

from django.urls import path

from .views import *


urlpatterns = [
    path('proxy/', GetProxyInfo.as_view()),
    path('upload_file/', FileUploadView.as_view()),
]


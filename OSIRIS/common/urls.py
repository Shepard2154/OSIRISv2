from django.urls import path

from .views import *


urlpatterns = [
    path('proxy/', GetProxyInfo.as_view()),
]


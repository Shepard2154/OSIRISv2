from django.urls import include, path

from .views import *

urlpatterns = [
    path('proxy/', GetProxyInfo.as_view()),
]

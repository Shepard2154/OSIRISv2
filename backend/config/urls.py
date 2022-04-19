from django.urls import include, path

urlpatterns = [
    path('twitter/', include('twitter.urls')),
    path('common/', include('common.urls')),
]

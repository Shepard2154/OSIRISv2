from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('twitter/', include('twitter.urls')),
    path('common/', include('common.urls')),
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
]

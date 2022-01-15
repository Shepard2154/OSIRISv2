from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('osiris/', include('osiris.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

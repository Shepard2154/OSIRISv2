from django.contrib import admin
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="OSIRIS API",
      default_version='v1',
      description="OSIRIS API",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="john-shepard-2154@yandex.ru"),
      license=openapi.License(name="Protected"),
   ),
   public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('twitter/', include('twitter.urls')),
    path('common/', include('common.urls')),
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
]

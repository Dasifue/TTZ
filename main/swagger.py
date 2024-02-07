from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

url = settings.SWAGGER_BASE_URL

schema_view = get_schema_view(
    openapi.Info(
        title="TTZ API",
        default_version="v1",
        description="API service for TZ",
        contact=openapi.Contact(email="dasifue@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    url=url,
    permission_classes=(permissions.AllowAny,),
)

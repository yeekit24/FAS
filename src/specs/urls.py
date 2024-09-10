from django.urls import re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


swagger_info = openapi.Info(
    title="FAS API",
    default_version="v1",
    description="FAS description",
    contact=openapi.Contact(email="yeekit24@gmail.com")
)


schema_view = get_schema_view(
    swagger_info,
    public=True,
    authentication_classes=[],
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
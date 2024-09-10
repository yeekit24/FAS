from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("v1/api/", include("config.api_router", namespace="v1/api")),
    path(settings.ADMIN_URL, admin.site.urls),
    path("health-checks/", include("health_check.urls")),
]
    
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local asgi development
    urlpatterns += staticfiles_urlpatterns()

# Specify handlers to ensure errors happening within Django but outside the
# context of DRF are still JSON and in our expected format.
# https://docs.djangoproject.com/en/3.1/ref/urls/
handler400 = "src.utils.exception_handlers.bad_request"
handler403 = "src.utils.exception_handlers.permission_denied"
handler404 = "src.utils.exception_handlers.not_found"
handler500 = "src.utils.exception_handlers.server_error"

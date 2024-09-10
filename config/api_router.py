"""DRF router module."""

from rest_framework.routers import SimpleRouter
from django.urls import include, path

from src.applicants.view import ApplicantViewset
from src.schemes.view import SchemeViewset
from src.applications.view import ApplicationViewset

router = SimpleRouter(trailing_slash=False)
router.register("applicants", ApplicantViewset, "applicants")
router.register("schemes", SchemeViewset, "scheme")
router.register("applications", ApplicationViewset, "applications")

specs_url = [
    path("specs/", include("src.specs.urls")),
]


app_name = "fas"
urlpatterns = router.urls + specs_url

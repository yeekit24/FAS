"""DRF router module."""

from rest_framework.routers import SimpleRouter


from src.applicants.view import ApplicantViewset
from src.schemes.view import SchemeViewset
from src.users.view import UserViewset


router = SimpleRouter(trailing_slash=False)
router.register("applicants", ApplicantViewset, "applicants")
router.register("schemes", SchemeViewset, "scheme")
router.register("users", UserViewset, "user")


app_name = "fas"
urlpatterns = router.urls

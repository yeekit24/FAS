from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from src.applicants.models import Applicant
from src.schemes.models import Scheme, SchemeBenefit, SchemeCriteria
from src.users.models import User
from ..models import Application


class ApplicationViewSetTestCase(APITestCase):
    fixtures = ["dev.yaml"]

    def setUp(self):
        # This method runs before every test
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer 123")
        self.base_url = "/v1/api/applications"
        self.applicant = Applicant.objects.create(
            name="kelly ",
            marital_status="married",
            sex="male",
            employment_status="unemployed",
            date_of_birth="1990-01-01",
        )
        self.scheme = Scheme.objects.create(
            name="Give all unemployed with household kids 1000",
        )
        SchemeBenefit.objects.create(
            name="School free meals credit",
            amount=1000,
            apply_household=True,
            scheme_id=self.scheme,
        )
        SchemeCriteria.objects.create(
            name="All unemployed",
            ops="=",
            threshold="unemployed",
            field="employment_status",
            scheme_id=self.scheme,
        )
        self.user = User.objects.get(username="admin")
        self.application = Application.objects.create(
            applicant=self.applicant,
            scheme=self.scheme,
            reviewer=self.user,
            created_time=timezone.now(),
        )

    def test_create_application(self):
        data = {
            "applicant_uid": self.applicant.uid,
            "scheme_uid": self.scheme.uid,
            "reviewer": self.user.uid,
        }
        response = self.client.post(self.base_url, data, follow=True, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_application(self):
        response = self.client.get(self.base_url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["applicant"]["uid"], str(self.applicant.uid))

    def test_partial_update_application(self):
        data = {"status": "approved"}
        response = self.client.patch(
            f"{self.base_url}/{self.application.uid}", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], data["status"])

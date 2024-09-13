from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from ..models import Applicant, ApplicantHousehold


class ApplicantViewSetTestCase(APITestCase):
    fixtures = ['dev.yaml']

    def setUp(self):
        # This method runs before every test
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer 123')
        self.base_url = '/v1/api/applicants'
        self.applicant = Applicant.objects.create(
            name="kelly ",
            marital_status= "married",
            sex="male",
            employment_status="unemployed",
            date_of_birth="1990-01-01"
        )
        ApplicantHousehold.objects.create(
            name= "kelly son 24",
            relation= "son",
            date_of_birth= "2000-01-01",
            marital_status= "single",
            employment_status= "unemployed",
            sex= "male",
            applicant_id=self.applicant
        )

    def test_create_applicant(self):
        data = {
            "name": "kelly ",
            "households": [
                {
                    "name": "kelly son 24",
                    "relation": "son",
                    "date_of_birth": "2000-01-01",
                    "marital_status": "single",
                    "employment_status": "unemployed",
                    "sex": "male"
                },
                {
                    "name": "kelly daughter 15",
                    "relation": "daughter",
                    "date_of_birth": "2009-01-01",
                    "marital_status": "single",
                    "employment_status": "unemployed",
                    "sex": "female"
                }
            ],
            "marital_status": "married",
            "sex": "male",
            "employment_status": "unemployed",
            "date_of_birth": "1990-01-01"
        }
        response = self.client.post(self.base_url, data, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_applicant(self):
        response = self.client.get(self.base_url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.applicant.name)

    def test_partial_update_applicant(self):
        data = {"name": "random"}
        response = self.client.patch(f'{self.base_url}/{self.applicant.uid}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data["name"])

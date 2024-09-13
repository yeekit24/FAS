from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from ..models import Scheme, SchemeBenefit, SchemeCriteria


class SchemeViewSetTestCase(APITestCase):
    fixtures = ['dev.yaml']

    def setUp(self):
        # This method runs before every test
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer 123')
        self.base_url = '/v1/api/schemes'
        self.scheme = Scheme.objects.create(
            name="Give all unemployed with household kids 1000",
        )
        SchemeBenefit.objects.create(
            name="School free meals credit",
            amount=1000,
            apply_household=True,
            scheme_id=self.scheme
        )
        SchemeCriteria.objects.create(
            name="All unemployed",
            ops="=",
            threshold="unemployed",
            field="employment_status",
            scheme_id=self.scheme
        )


    def test_create_scheme(self):
        data = {
            "name": "Give all unemployed with household kids 1000",
            "benefits":[{
                
                "amount": 1000,
                "apply_household": True
            }],
            "criterias": [{
                "name": "All unemployed",
                "ops": "=",
                "threshold": "unemployed",
                "field": "employment_status"
            },
            {
                "name": "Household kids",
                "ops": "<=",
                "threshold": "16",
                "field": "age",
                "apply_household": True
            }
            ]
        }
        response = self.client.post(self.base_url, data, follow=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_scheme(self):
        response = self.client.get(self.base_url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Give all unemployed with household kids 1000")

    def test_partial_update_scheme(self):
        data = {"name": "random"}
        response = self.client.patch(f'{self.base_url}/{self.scheme.uid}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data["name"])

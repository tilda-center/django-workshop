from django.shortcuts import reverse

from rest_framework.test import APITestCase
from v1.factories.verify_token import VerifyTokenFactory

class VerifyTokenTestCase(APITestCase):
    def setUp(self):
        self.verify_token = VerifyTokenFactory()
        self.path = reverse(
                'verifytoken-detail', 
                kwargs={
                    'pk': self.verify_token.token,
                    }
                )

    def test_get_success(self):
        response = self.client.get(self.path)
        print(response.data)



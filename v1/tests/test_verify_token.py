import uuid
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
        self.assertEqual(str(self.verify_token.token), response.data['token'])
        self.assertEqual(self.verify_token.email, response.data['email'])
 
    def test_update_success_and_test_token_is_used(self):
        response = self.client.put(self.path)
        self.assertEqual(response.status_code, 200)
        self.verify_token.refresh_from_db()
        self.assertEqual(self.verify_token.used, True)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)
    
    def test_fail_404(self):
        path = reverse(
                'verifytoken-detail', 
                kwargs={
                    'pk': str(uuid.uuid4()),
                    }
                )
        response = self.client.get(path)
        self.assertEqual(response.status_code, 404)


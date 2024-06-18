import jwt
from django.shortcuts import reverse

from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.path = reverse('register-list')

    def test_success_register(self):
        data = {
            'email': 'test1@test.com',
            'password': 'Test123123123!',
        }
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 200)
        access_token_data = jwt.decode(
            response.data['access'],
            options={
                'verify_signature': False
            }
        )
        refresh_token_data = jwt.decode(
            response.data['refresh'],
            options={
                'verify_signature': False
            }
        )
        self.assertEqual(access_token_data['roles'], ['student'])
        self.assertEqual(refresh_token_data['roles'], ['student'])

import jwt
from django.shortcuts import reverse
from django.contrib.auth.models import Group
from v1.factories.user import UserFactory

from rest_framework.test import APITestCase


class RefreshTestCase(APITestCase):
    def setUp(self):
        self.login_path = reverse('token_obtain_pair')
        self.refresh_path = reverse('token_refresh')
        self.user = UserFactory()
        self.user.set_password('Test123123!')
        self.user.save()
        self.group = Group.objects.create(name='student')
        self.user.groups.set([self.group])

    def test_success_refresh(self):
        data = {
            'username': self.user.username,
            'password': 'Test123123!',
        }
        response = self.client.post(self.login_path, data)
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

        # test refresh logic
        data = {
            'refresh': response.data['refresh'],
        }
        response = self.client.post(self.refresh_path, data)
        access_token_data = jwt.decode(
            response.data['access'],
            options={
               'verify_signature': False
            }
        )
        self.assertEqual(access_token_data['roles'], ['student'])
        import pdb; pdb.set_trace()

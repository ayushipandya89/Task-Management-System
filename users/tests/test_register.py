from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.constants import USER_CREATED
from users.models import CustomUser


class RegisterViewTests(APITestCase):
    """
    Tests for the user registration endpoint.
    """

    def setUp(self):
        self.url = reverse('register_user')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Test@1234',
            'is_admin': False,
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.invalid_payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'short',
            'is_admin': False,
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_register_user_success(self):
        """
        Test successful user registration.
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], USER_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_register_user_failure(self):
        """
        Test registration failure due to invalid password.
        """
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser


class LoginViewTests(APITestCase):
    """
    Tests for the user login endpoint.
    """

    def setUp(self):
        self.url = reverse('login')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Test@1234'
        )
        self.valid_payload = {
            'username': 'testuser',
            'password': 'Test@1234'
        }
        self.invalid_payload = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

    def test_login_success(self):
        """
        Test successful user login and token generation.
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure(self):
        """
        Test login failure due to incorrect credentials.
        """
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'No active account found with the given credentials')


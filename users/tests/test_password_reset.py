from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core import mail

from users.constants import PASSWORD_RESET_SUCCESSFULLY
from users.models import CustomUser


class PasswordResetRequestViewTests(APITestCase):
    """
    Tests for the password reset request endpoint.
    """

    def setUp(self):
        self.url = reverse('password_reset_request')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Test@1234'
        )
        self.valid_payload = {
            'email': 'testuser@example.com'
        }
        self.invalid_payload = {
            'email': 'invaliduser@example.com'
        }

    def test_password_reset_request_success(self):
        """
        Test successful password reset request.
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], PASSWORD_RESET_SUCCESSFULLY)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_request_failure(self):
        """
        Test failure of password reset request due to non-existent email.
        """
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'No user found with this email address.')

